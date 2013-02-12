from random import choice

def exampleChooser(request, test):
    try:
        # do whatever you want here, but return one experiment from the test
        return choice(test.experiments.filter(active=True))
    except:
        return None