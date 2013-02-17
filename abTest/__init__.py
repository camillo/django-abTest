from logging import getLogger
from models import Goal, Experiment, Test

from django.conf import settings
from django.shortcuts import render_to_response
from abTest.settings import AB_TEST_REQUEST_NAME, AB_TEST_LOGGER

logger = getLogger(AB_TEST_LOGGER)

def render_to_ab_response(abTest, templates, dictionary=None, defaultTemplate = None, context_instance=None):
    targetTemplate = defaultTemplate
    for test, result in abTest.items():
        if result.experiment.name in templates:
            targetTemplate = templates[result.experiment.name]
            break
    return render_to_response(targetTemplate, dictionary, context_instance = context_instance)

def reachedGoal(request, name, commit = True, failSilent=None):
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

def goalReached(request, name, commit = True, failSilent=None):
    """
    deprecated: use reachedGoal instead
    """
    return reachedGoal(request, name, commit, failSilent)

def setExperiment(request, test, experiment):
    if not isinstance(test, Test):
        test = Test.objects.get(name = test)
    if not isinstance(experiment, Experiment):
        experiment = Experiment.objects.get(name = experiment)

    for currentTest, currentResult in getattr(request, AB_TEST_REQUEST_NAME, {}).items():
        if not currentTest == test: continue
        if experiment in currentTest.experiments.all():
            currentResult.experiment = experiment
            currentResult.save()
            logger.debug("set experiment for test [%s] to: [%s]", test, experiment)
            break