class StringFacade(str):
    def __init__(self, raw):
        str.__init__(self, raw.name)
        self.raw = raw

def ab(request):
    experiments = {}
    for test, result in request.abTest.items():
        experiments[StringFacade(test)] = StringFacade(result.experiment)
    return {'ab' : experiments}
