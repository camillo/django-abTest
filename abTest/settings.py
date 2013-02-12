from django.conf import settings
from random import choice

AB_TEST_EXPERIMENT_CHOOSER = getattr(settings, 'AB_TEST_EXPERIMENT_CHOOSER', lambda request, test: choice(test.experiments.filter(active=True)))

