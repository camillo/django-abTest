from logging import getLogger
from settings import AB_TEST_REQUEST_NAME, AB_TEST_CONTEXT_NAME, AB_TEST_FAIL_SILENT_CONTEXT, AB_TEST_LOGGER_CONTEXT

class StringFacade(str):
    def __init__(self, raw):
        str.__init__(self, raw.name)
        self.raw = raw

class TestFacade(StringFacade):
    def __init__(self, raw):
        StringFacade.__init__(self, raw)

    @property
    def goals(self):
        return self.raw.goals.all()

class ExperimentFacade(StringFacade):
    def __init__(self, raw):
        StringFacade.__init__(self, raw)
        self.test = None

    @property
    def experiments(self):
        if not self.test:
            return None
        return self.test.experiments.all()

logger = getLogger(AB_TEST_LOGGER_CONTEXT)

def ab(request):
    #noinspection PyBroadException
    try:
        if hasattr(request, AB_TEST_REQUEST_NAME):
            experiments = {}
            for test, result in getattr(request, AB_TEST_REQUEST_NAME).items():
                exp = ExperimentFacade(result.experiment)
                exp.test = test
                experiments[TestFacade(test)] = exp
            return {AB_TEST_CONTEXT_NAME : experiments}
    except Exception as ex:
        logger.error("error, putting abTest [%s] into context: %s", AB_TEST_CONTEXT_NAME, ex)
        if not AB_TEST_FAIL_SILENT_CONTEXT:
            raise

    return {}
