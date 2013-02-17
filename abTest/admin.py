from django.shortcuts import render_to_response, RequestContext
from  django.contrib import admin
from django.utils.functional import update_wrapper
from models import Experiment, Goal,Test,TestResult, StatisticRow
from django.utils.translation import ugettext_lazy as _

class TestAdmin(admin.ModelAdmin):
    def get_urls(self):
        from django.conf.urls import patterns, url
        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name
        print "name:%s_%s_stats" % info
        return patterns('',
            url(r'^stats/(.*)/$', wrap(self.stats), name='%s_%s_stats' % info),
            url(r'^setExperiment/(.+)/(.+)/$', 'abTest.views.adminSetExperiment', name='%s_%s_setExperiment' % info),
            url(r'^clearSession/$', 'abTest.views.adminClear', name='%s_%s_clearSession' % info),
        ) + super(TestAdmin, self).get_urls()

    def stats(self, request, test):
        return render_to_response('admin/abTest/test/statistic.html', {
            'title': _('Statistics'),
            }, context_instance=RequestContext(request))

admin.site.register(Experiment)
admin.site.register(Goal)
admin.site.register(Test, TestAdmin)
admin.site.register(TestResult)
admin.site.register(StatisticRow)

