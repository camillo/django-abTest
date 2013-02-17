from logging import getLogger
from django.db import models
from abTest import settings
from django.template.defaultfilters import slugify


class Goal(models.Model):
    name = models.CharField(max_length=50, unique=True)
    value = models.IntegerField(default=1)
    slug = models.SlugField(editable=False)

    def reached(self, request, commit = True):
        ret = []
        for test, result in getattr(request, settings.AB_TEST_REQUEST_NAME, {}).items():
            if result.finished: continue
            if self in test.goals.all() and not self in result.goals.all():
                result.goals.add(self)
                ret.append([test, result])
                if commit:
                    result.save()
        return ret

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        models.Model.save(self, force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    name = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(editable=False)

    def __unicode__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        models.Model.save(self, force_insert, force_update, using, update_fields)

class Test(models.Model):
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField()
    goals = models.ManyToManyField(Goal)
    experiments = models.ManyToManyField(Experiment)
    slug = models.SlugField(editable=False)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.slug:
            self.slug = slugify(self.name)
        models.Model.save(self, force_insert, force_update, using, update_fields)

    def __unicode__(self):
        return self.name

class TestResult(models.Model):
    test = models.ForeignKey(Test)
    experiment = models.ForeignKey(Experiment)
    goals = models.ManyToManyField(Goal, blank=True)
    finished = models.BooleanField()

    @classmethod
    def chooseExperiment(cls, request, test, commit=True):
        #noinspection PyBroadException
        try:
            chooser = settings.AB_TEST_EXPERIMENT_CHOOSER
            experiment = chooser(request, test)
            ret = TestResult.objects.create(test = test, experiment = experiment, finished = False)
            if commit:
                ret.save()
            return ret
        except Exception as ex:
            getLogger(settings.AB_TEST_LOGGER).error("error, choosing experiment for test [%s]: %s", test, ex)
            raise


    @property
    def reachedGoal(self):
        return len(self.goals.all()) > 0

    def __unicode__(self):
        return "%s - %s" % (self.test, self.experiment)

class GoalStatisticRow(models.Model):
    goal = models.ForeignKey(Goal)
    reached = models.IntegerField()

class ExperimentStatisticRow(models.Model):
    experiment = models.ForeignKey(Experiment)
    runs = models.IntegerField()
    reached = models.IntegerField()
    goalDetails = models.ManyToManyField(GoalStatisticRow)

    def __unicode__(self):
        return self.experiment.name

class StatisticRow(models.Model):
    test = models.ForeignKey(Test)
    runs = models.IntegerField()
    result = models.ManyToManyField(ExperimentStatisticRow)
    created = models.DateTimeField(auto_now=True)

    @classmethod
    def createStatistic(cls, testResults, commit = False):
        if not testResults: return None
        test = testResults[0].test
        ret = StatisticRow.objects.create(test = test, runs = len(testResults))
        try:
            experimentRows = {}
            for result in testResults:
                if not result.test == test:
                    raise Exception("All testResults must be for the same test.")
                experiment = result.experiment
                if experiment in experimentRows:
                    experimentRow = experimentRows[experiment]
                    experimentRow.runs += 1
                else:
                    experimentRow = ExperimentStatisticRow.objects.create(experiment = experiment, runs = 1, reached = 0)
                    experimentRows[experiment] = experimentRow
                    ret.result.add(experimentRow)
                for goal in result.goals.all():
                    if experimentRow.goalDetails.filter(goal = goal).exists():
                        goalRow = experimentRow.goalDetails.get(goal = goal)
                        goalRow.reachd += 1
                    else:
                        goalRow = GoalStatisticRow.objects.create(goal = goal, reached = 1)
                        experimentRow.goalDetails.add(goalRow)

            if commit:
                ret.save()
                for result in testResults:
                    result.delete()
            return ret
        except:
            ret.delete()
            raise
