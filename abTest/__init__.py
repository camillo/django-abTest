from logging import getLogger
from models import Goal, Experiment

from django.conf import settings
from django.shortcuts import render_to_response

logger = getLogger(getattr(settings, 'AB_TEST_LOGGER',"abTest"))

def render_to_ab_response(abTest, templates, dictionary=None, defaultTemplate = None, context_instance=None):
    targetTemplate = defaultTemplate
    for test, result in abTest.items():
        if result.experiment.name in templates:
            targetTemplate = templates[result.experiment.name]
            break
    return render_to_response(targetTemplate, dictionary, context_instance = context_instance)

def goalReached(request, name, commit = True, failSilent=None):
    #noinspection PyBroadException
    if failSilent is None:
        failSilent = not getattr(settings,'DEBUG', True)
    try:
        goal = Goal.objects.get(name = name)
        return goal.reached(request, commit)
    except Exception as ex:
        logger.error('was not able to reach goal [%s]: %s', name, ex)
        if not failSilent:
            raise
        return []

def setExperiment(request, name):
    experiment = Experiment.objects.get(name=name)
    for test, result in request.abTest.items():
        if experiment in test.experiments.all():
            result.experiment = experiment
            result.save()