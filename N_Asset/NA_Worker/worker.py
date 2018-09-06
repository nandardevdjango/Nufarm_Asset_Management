class NATaskWorker(object):
    def __init__(self, func, args=[], kwargs={}):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def run(self):
        if callable(self.func):
            return self.func.delay(*self.args, **self.kwargs)
