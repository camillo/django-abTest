from django import template
from django.conf import settings
from django.core.urlresolvers import reverse
register = template.Library()

def getAb(context):
    #todo: for any reason I am not able to import abTest.settings
    contextName = getattr(
        settings, 'AB_TEST_CONTEXT_NAME',
        getattr(settings, 'AB_TEST_DEFAULT_KEY_NAME', 'ab'))
    if not context.has_key(contextName):
        return None
    return context.get(contextName)


def getExperiment(context, experiment):
    ab = getAb(context)
    if ab is None: return ""
    if not ab.has_key(experiment):
        return ""
    return ab.get(experiment)

@register.simple_tag(takes_context=True)
def reachedGoalUrl(context, goalName):
    ab = getAb(context)
    if ab is None: return ""
    for test in ab:
        for goal in test.goals:
            if goal.name == goalName:
                return reverse("abTest:reachedGoal", args=[goal.slug,])
    return ""

register.assignment_tag(getExperiment, takes_context=True)