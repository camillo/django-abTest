def ab(request):
    experiments = {}
    for test, result in request.abTest.items():
        experiments[test.name] = result.experiment.name
    return {'ab' : experiments}
