from django.conf import settings
from random import choice

# If set to False, ab-test framework is deactivated. No experiments get chosen, no information is written
# into session, request and context; no TestResults get created
AB_TEST_ACTIVE = getattr(settings, 'AB_TEST_ACTIVE', True)

# Per default, middleware choose randomly one experiment; you may define your own function here.
# You may return any Experiment from the test, but it is recommended to not return inactive experiments.
AB_TEST_EXPERIMENT_CHOOSER = getattr(settings, 'AB_TEST_EXPERIMENT_CHOOSER',
    lambda request, test: choice(test.experiments.filter(active=True)))

# If set to True, abTest framework will not raise exceptions (they are still logged).
# Per default, exceptions will be eaten in live deployment (ab testing should not break your side),
# put raised with DEBUG = True
AB_TEST_FAIL_SILENT = getattr(settings, 'AB_TEST_FAIL_SILENT', not settings.DEBUG)

# Fail silent for context processor
AB_TEST_FAIL_SILENT_CONTEXT = getattr(settings, 'AB_TEST_FAIL_SILENT_CONTEXT', AB_TEST_FAIL_SILENT)

# Fail silent for middleware
AB_TEST_FAIL_SILENT_MIDDLEWARE = getattr(settings, 'AB_TEST_FAIL_SILENT_MIDDLEWARE', AB_TEST_FAIL_SILENT)

# The default key name, used in dictionaries.
AB_TEST_DEFAULT_KEY_NAME = getattr(settings, 'AB_TEST_DEFAULT_KEY_NAME', 'ab')

# These settings defines the keys for dictionaries in session, request and context
AB_TEST_CONTEXT_NAME = getattr(settings, 'AB_TEST_CONTEXT_NAME', AB_TEST_DEFAULT_KEY_NAME)
AB_TEST_SESSION_NAME = getattr(settings, 'AB_TEST_SESSION_NAME', AB_TEST_DEFAULT_KEY_NAME)
AB_TEST_REQUEST_NAME = getattr(settings, 'AB_TEST_REQUEST_NAME', AB_TEST_DEFAULT_KEY_NAME)

# Define the redirect targets for views here.
# They are used, if no next parameter is provided. If not configured, views tries to navigate back; if no
# HTTP_REFERER is set, AB_TEST_REDIRECT_AFTER_DEFAULT is used.
AB_TEST_REDIRECT_AFTER_DEFAULT = getattr(settings, 'AB_TEST_REDIRECT_AFTER_DEFAULT', '/')
AB_TEST_REDIRECT_AFTER_SET_EXPERIMENT = getattr(settings, 'AB_TEST_REDIRECT_AFTER_SET_EXPERIMENT', None)
AB_TEST_REDIRECT_AFTER_CLEAR_SESSION = getattr(settings, 'AB_TEST_REDIRECT_AFTER_CLEAR_SESSION', None)
AB_TEST_REDIRECT_AFTER_REACHED_GOAL = getattr(settings, 'AB_TEST_REDIRECT_AFTER_REACHED_GOAL', None)

# This template is used to render the session admin page.
# It is NOT used in 'normal' django admin, but in provided view sessionAdmin
# default is 'abTest/sessionAdmin.html'
AB_TEST_SESSION_ADMIN_TEMPLATE = getattr(settings, 'AB_TEST_REDIRECT_AFTER_CLEAR_SESSION', 'abTest/sessionAdmin.html')

# configure access to your debug views. Valid entries in list are:
# 1. the string 'debug' - this allows unlimited access if we are in debug mode
# 2. the string 'staff' - this allows unlimited access, if user is in group 'staff'
# 3. the string 'superuser' - this allows unlimited access to superuser.
# 4. the string 'all' - everything is allowed for everyone
# 5. a callable (lambda expression, for example), that accepts a user and returns True or False.
#
# Default is ('debug', 'staff')
AB_TEST_DEBUG_VIEWS_RESTRICTIONS = getattr(settings, 'AB_TEST_DEBUG_VIEWS_RESTRICTIONS', ('debug','staff'))

# You may define the used logger here
AB_TEST_LOGGER = getattr(settings, 'AB_TEST_LOGGER', 'abTest')
AB_TEST_LOGGER_CONTEXT = getattr(settings, 'AB_TEST_LOGGER_CONTEXT', AB_TEST_LOGGER + '.context')
AB_TEST_LOGGER_MIDDLEWARE = getattr(settings, 'AB_TEST_LOGGER_MIDDLEWARE', AB_TEST_LOGGER + '.middleware')
AB_TEST_LOGGER_DEBUG_VIEWS = getattr(settings, 'AB_TEST_LOGGER_DEBUG_VIEWS', AB_TEST_LOGGER + '.debugViews')