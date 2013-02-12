from random import choice
from django.db import models
from django.core.exceptions import ValidationError

class Goal(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def reached(self, request, commit = True):
        ret = []
        for test, result in request.abTest.items():
            if result.finished: continue
            if self in test.goals.all() and not self in result.goals.all():
                result.goals.add(self)
                ret.append([test, result])
                if commit:
                    result.save()
        return ret

    def __unicode__(self):
        return self.name

class Experiment(models.Model):
    name = models.CharField(max_length=20, unique=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Test(models.Model):
    name = models.CharField(max_length=50, unique=True)
    active = models.BooleanField()
    goals = models.ManyToManyField(Goal)
    experiments = models.ManyToManyField(Experiment)

    def __unicode__(self):
        return self.name

class TestResult(models.Model):
    test = models.ForeignKey(Test)
    experiment = models.ForeignKey(Experiment)
    goals = models.ManyToManyField(Goal, blank=True)
    finished = models.BooleanField()

    @classmethod
    def createRandom(cls, test, commit=True):
        experiment = choice(test.experiments.filter(active=True))
        ret = TestResult.objects.create(test = test, experiment = experiment, finished = False)
        if commit:
            ret.save()
        return ret

    @property
    def reachedGoal(self):
        return len(self.goals.all()) > 0

    def __unicode__(self):
        return "%s - %s" % (self.test, self.experiment)
