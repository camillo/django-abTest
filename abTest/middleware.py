from models import Test, TestResult
from logging import getLogger
from settings import AB_TEST_ACTIVE, AB_TEST_LOGGER_MIDDLEWARE, AB_TEST_SESSION_NAME, AB_TEST_REQUEST_NAME, AB_TEST_FAIL_SILENT_MIDDLEWARE

class ABTestRequest(dict):

    def __getattr__(self,name):
        """
        Make the values (the testResults) available per name.
        """
        for key, value in self.items():
            if key.name == name:
                return value.experiment

class RequestMiddleware(object):

    def process_request(self, request):
        #noinspection PyBroadException
        if not AB_TEST_ACTIVE:
            return None
        try:
            sessionTests = request.session.get(AB_TEST_SESSION_NAME, {})
            if sessionTests is None: sessionTests = {}
            newSessionTests = {}
            requestTests = ABTestRequest()
            for activeTest in Test.objects.filter(active=True):
                if activeTest.pk in sessionTests and TestResult.objects.filter(pk=sessionTests[activeTest.pk]).exists():
                    activeTestResult = TestResult.objects.get(pk=sessionTests[activeTest.pk])
                else:
                    activeTestResult = TestResult.chooseExperiment(request, activeTest)
                newSessionTests[activeTest.pk] = activeTestResult.pk
                requestTests[activeTest] = activeTestResult
            request.session[AB_TEST_SESSION_NAME] = newSessionTests
            setattr(request, AB_TEST_REQUEST_NAME, requestTests)
        except Exception as ex:
            getLogger(AB_TEST_LOGGER_MIDDLEWARE).error("error processing request: %s", ex)
            if not AB_TEST_FAIL_SILENT_MIDDLEWARE:
                raise

        return None



