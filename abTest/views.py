from django.shortcuts import Http404, HttpResponseRedirect, RequestContext, render_to_response, HttpResponse
from abTest import setExperiment as _setExperiment
from models import Experiment
from django.conf import settings
from middleware import SESSION_NAME

def setExperiment(request, name = None):

    name = name or request.REQUEST.get('name', None)
    if not name:
        raise Http404
    try:
        _setExperiment(request, name)
    except Experiment.DoesNotExist:
        raise Http404
    if request.is_ajax():
        return HttpResponse('ok')
    next = request.REQUEST.get("next",
        getattr(settings, 'AB_TEST_REDIRECT_AFTER_SET_EXPERIMENT',
        request.META.get('HTTP_REFERER',
        '/')))
    return HttpResponseRedirect(next)

def clear(request):
    request.abTest = {}
    request.session[SESSION_NAME] = {}
    if request.is_ajax():
        return HttpResponse('ok')
    next = request.REQUEST.get("next",
        getattr(settings, 'AB_TEST_REDIRECT_AFTER_CLEAR',
            request.META.get('HTTP_REFERER',
                '/')))

    return HttpResponseRedirect(next)

def sessionAdmin(request):
    context = RequestContext(request)
    return render_to_response("abTest/sessionAdmin.html", context_instance = context)