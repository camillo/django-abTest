from models import Test, TestResult

SESSION_NAME = 'abTest'

class ABTestRequest(dict):
    def __getattr__(self,name):
        for key, value in self.items():
            if key.name == name:
                return value.experiment.name

class RequestMiddleware(object):

    def process_request(self, request):
        #noinspection PyBroadException
        try:
            sessionTests = request.session.get(SESSION_NAME, {})
            if sessionTests is None: sessionTests = {}
            newSessionTests = {}
            requestTests = ABTestRequest()
            for activeTest in Test.objects.filter(active=True):
                if activeTest.pk in sessionTests:
                    try:
                        activeTestResult = TestResult.objects.get(pk=sessionTests[activeTest.pk])
                    except TestResult.DoesNotExist:
                        activeTestResult = TestResult.createRandom(request, activeTest)
                else:
                    activeTestResult = TestResult.createRandom(request, activeTest)
                newSessionTests[activeTest.pk] = activeTestResult.pk
                requestTests[activeTest] = activeTestResult
            request.session[SESSION_NAME] = newSessionTests
            request.abTest = requestTests
        except Exception as ex:
            print "ex!!: %s" % ex
            pass #todo: log? our middleware should not break the application

        return None



