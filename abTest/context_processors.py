class StringFacade(str):
    def __init__(self, raw):
        str.__init__(self, raw.name)
        self.raw = raw

class TestFacade(StringFacade):
    def __init__(self, raw):
        StringFacade.__init__(self, raw)

class ExperimentFacade(StringFacade):
    def __init__(self, raw):
        StringFacade.__init__(self, raw)
        self.test = None

    @property
    def experiments(self):
        if not self.test:
            return None
        return self.test.experiments.all()

def ab(request):
    experiments = {}
    for test, result in request.abTest.items():
        exp = ExperimentFacade(result.experiment)
        exp.test = test
        experiments[TestFacade(test)] = exp
    return {'ab' : experiments}
