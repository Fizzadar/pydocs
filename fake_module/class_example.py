'''
Example classes for pydocs.
'''

class ExampleClass(object):
    '''This ExampleClass does something magical.'''
    def __init__(self, test, *args, **kargs):
        pass

    def some_function(self):
        '''Example function inside a class.'''
        pass


class TestException(Exception):
    pass
