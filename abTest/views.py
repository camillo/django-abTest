from django.shortcuts import Http404, HttpResponseRedirect, RequestContext, render_to_response, HttpResponse
from django.contrib.auth.decorators import user_passes_test, PermissionDenied, wraps,available_attrs
from abTest import setExperiment as _setExperiment
from abTest.models import Goal, Test, Experiment
from logging import getLogger
from django.conf import settings

from abTest.settings import AB_TEST_SESSION_NAME, AB_TEST_CONTEXT_NAME, AB_TEST_REDIRECT_AFTER_SET_EXPERIMENT, \
    AB_TEST_REDIRECT_AFTER_DEFAULT, AB_TEST_REDIRECT_AFTER_CLEAR_SESSION, AB_TEST_FAIL_SILENT, AB_TEST_LOGGER_DEBUG_VIEWS, \
    AB_TEST_SESSION_ADMIN_TEMPLATE, AB_TEST_DEBUG_VIEWS_RESTRICTIONS, AB_TEST_REDIRECT_AFTER_REACHED_GOAL

logger = getLogger(AB_TEST_LOGGER_DEBUG_VIEWS)

def _redirectOrAck(request, settingsKey, message="ok"):
    if request.is_ajax():
        return HttpResponse(message)

    next = request.REQUEST.get("next", settingsKey) or \
           request.META.get('HTTP_REFERER', AB_TEST_REDIRECT_AFTER_DEFAULT)
    return HttpResponseRedirect(next)

def reachedGoal(request, goal):
    try:
        goal = Goal.objects.get(slug=goal)
        goal.reached(request)
        logger.info("reached goal: %s", goal)
        return _redirectOrAck(request, AB_TEST_REDIRECT_AFTER_REACHED_GOAL)
    except Goal.DoesNotExist:
        raise Http404
    except Exception as ex:
        logger.error("error reaching goal: %s", ex)
        if not AB_TEST_FAIL_SILENT:
            raise

# =============================
#  Debug and admin stuff below
# =============================

class InvalidRestrictionException(Exception):
    pass

#noinspection PyUnusedLocal
def _guard(*args, **kwargs):
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            letPass = False
            for restriction in AB_TEST_DEBUG_VIEWS_RESTRICTIONS:
                if callable(restriction):
                    guard = restriction
                else:
                    name = restriction.lower()
                    if name == "debug":
                        guard = lambda u: settings.DEBUG
                    elif name == "staff":
                        guard = lambda u: u.is_staff
                    elif name == "superuser":
                        guard = lambda u: u.is_superuser
                    elif name == "all":
                        guard = lambda u: True
                    else:
                        msg = "invalid value [%s] in AB_TEST_DEBUG_VIEWS_RESTRICTIONS" % restriction
                        logger.error(msg)
                        if not AB_TEST_FAIL_SILENT:
                            raise InvalidRestrictionException(msg)
                        guard = lambda u: False
                letPass = guard(user)
                if letPass: break
            if letPass:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator

def adminSetExperiment(request, testPk, experimentPk):
    try:
        test = Test.objects.get(pk = testPk)
        experiment = Experiment.objects.get(pk=experimentPk)
        _setExperiment(request, test, experiment)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    except Test.DoesNotExist, Experiment.DoesNotExist:
        raise Http404

@_guard()
def setExperiment(request, testSlug, experimentSlug):
    try:
        test = Test.objects.get(slug = testSlug)
        experiment = Experiment.objects.get(slug=experimentSlug)
        _setExperiment(request, test, experiment)
    except Test.DoesNotExist, Experiment.DoesNotExist:
        raise Http404

    return _redirectOrAck(request, AB_TEST_REDIRECT_AFTER_SET_EXPERIMENT)

def adminClear(request):
    request.abTest = {}
    request.session[AB_TEST_SESSION_NAME] = {}
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@_guard()
def clear(request):
    request.abTest = {}
    request.session[AB_TEST_SESSION_NAME] = {}

    return _redirectOrAck(request, AB_TEST_REDIRECT_AFTER_CLEAR_SESSION)

@_guard()
def sessionAdmin(request):
    """
    Render the generic session admin.
    """
    context = RequestContext(request)
    if not context.has_key(AB_TEST_CONTEXT_NAME):
        msg = 'abTest context processor needs to be added in settings, to use session admin.'
        logger.error(msg)
        if not AB_TEST_FAIL_SILENT:
            raise Exception(msg)

    return render_to_response(AB_TEST_SESSION_ADMIN_TEMPLATE,{'ab' : context.get(AB_TEST_CONTEXT_NAME, {})},
        context_instance = context)

