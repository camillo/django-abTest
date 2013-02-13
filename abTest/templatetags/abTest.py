from django import template

register = template.Library()

@register.simple_tag
def getExperiment(ab, experiment):
    return ab[experiment]
