from  django.contrib import admin
from models import Experiment, Goal,Test,TestResult

admin.site.register(Experiment)
admin.site.register(Goal)
admin.site.register(Test)
admin.site.register(TestResult)

