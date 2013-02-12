from django.shortcuts import render_to_response, HttpResponse, RequestContext, HttpResponseRedirect
from django.contrib.messages import success
from abTest import goalReached, render_to_ab_response
from abTest.middleware import SESSION_NAME
from abTest.models import Test, TestResult, Goal, Experiment

def contact(request):
    context = RequestContext(request)
    return render_to_response("contact.html", context_instance = context)


def home(request):
    context = RequestContext(request)
    return render_to_response("home.html", context_instance = context)

def createLiveDemoData(request):
    if request.method == "POST":
        test = Test.objects.create(name = "background", active = True)
        test.goals.add(Goal.objects.create(name = "buttonPressed"))
        test.experiments.add(Experiment.objects.create(name="red"))
        test.experiments.add(Experiment.objects.create(name="blue"))
        test.experiments.add(Experiment.objects.create(name="green"))
        test.save()
        success(request, "Created live demo test data.")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    context = RequestContext(request)
    return render_to_response("createLiveDemoData.html", context_instance = context)

def liveDemo(request):
    if not Test.objects.filter(name = "background").exists():
        return createLiveDemoData(request)
    context = RequestContext(request)
    testResults = {}
    for test in Test.objects.filter(active = True):
        testResult = {}
        results = TestResult.objects.filter(test = test)
        testResult['count'] = len(results)
        reachedTotal = 0
        experiments = {}
        for experiment in test.experiments.all():
            experimentResult = {}
            allRuns = results.filter(experiment = experiment)
            experimentResult['count'] = len(allRuns)
            reachedGoals = 0
            for run in allRuns:
                reachedGoals += len(run.goals.all())
            experimentResult['reachedGoals'] = reachedGoals
            experiments[experiment] = experimentResult
            reachedTotal += reachedGoals

        testResult['reachedGoals'] = reachedTotal
        testResult['experiments'] = experiments
        testResults[test] = testResult
        print "%s" % testResults
    return render_to_response("liveDemo.html", {'testResults' : testResults, 'site':'liveDemo'}, context_instance = context)

def reachedGoalButton(request):
    """
    Earn a lot of money here, and set reached goal
    """

    goalReached(request, "buttonPressed")
    success(request, "thx for your money...")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def models(request):
    context = RequestContext(request)
    return render_to_response("models.html", {'site':'models'}, context_instance = context)

def usage(request):
    context = RequestContext(request)
    return render_to_response("usage.html", {'site':'usage'}, context_instance = context)

def home_old(request):
    if request.method == "POST":
        #get money here ....
        goalReached(request, "example Goal")

        return HttpResponse("thx for your money...")
    context = RequestContext(request)
    return render_to_ab_response(request.abTest, {
        'red' : 'abTest/red.html',
        'blue' : 'abTest/blue.html',
        'black' : 'abTest/black.html',
    }, defaultTemplate="abTest/example.html", context_instance=context)
    #return render_to_response("abTest/example.html", context_instance = context)

