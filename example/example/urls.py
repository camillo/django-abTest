from django.conf.urls import patterns, include, url
from django.contrib import admin
from abTest import urls as abTestUrls
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'abWeb.views.home', name='home'),
    url(r'^liveDemo/$', 'abWeb.views.liveDemo', name='liveDemo'),
    url(r'^clearSession/$', 'abWeb.views.clearSession', name='clearSession'),
    url(r'^spendMoney/$', 'abWeb.views.reachedGoalButton', name='spendMoney'),
    url(r'^usage/$', 'abWeb.views.usage', name='usage'),
    url(r'^models/$', 'abWeb.views.models', name='models'),
    url(r'^contact/$', 'abWeb.views.contact', name='contact'),
    url(r'^abTest/', include(abTestUrls, namespace="abTest")),

    url(r'^admin/', include(admin.site.urls)),
)
