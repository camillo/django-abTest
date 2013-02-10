# **********************************************************
# interesting stuff

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware', # <- *****************************************
    'abTest.middleware.RequestMiddleware', # <- It is VERY important to put abTest AFTER SessionMiddleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django.contrib.admin',
              # ****************************
    'abTest', # <- this is the required app

    'abWeb',  # <- this is only the example docu website
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    # Stuff above is default, if TEMPLATE_CONTEXT_PROCESSORS is not set.
    "abTest.context_processors.ab", # <- OPTIONAL: write dictionary [ab] into context, containing chosen experiment's name for every active test.
    "django.core.context_processors.request",  # <- OPTIONAL: Our middleware writes full models into request. If simple
                                               # checks as provided by [test] processor below, are not enough for your
                                               # needs, add the request processor. Find dict with active tests and chosen
                                               # experiments in request.abTest.
    )

# **********************************************************
# boring stuff

DEBUG = True
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = 'i-0duvgm34h)!o2*-ypil*#(#2_p4*p25s7rye@q!-1ndjd1+0'
ROOT_URLCONF = 'example.urls'
STATIC_URL = '/static/'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/django_ABTest.db',
        }
}

TEMPLATE_LOADERS = (
    'django.template.loaders.app_directories.Loader',
    )
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

