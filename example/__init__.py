'''
Welcome to the pydocs example.
'''


def function():
    '''An example function.'''
    pass

def args_function(arg1, arg2, *args):
    '''Another example with no-default arguments & some varargs.'''
    pass

def kwargs_function(key=None, something=True, **kwargs):
    '''A function with keyword arguments & a keywords argument.'''
    pass

def combined_function(arg1, key=True, something='another', *the_rest, **keywords):
    '''A function combining all of the above.'''
    pass

def wip_arg_comments(arg1, key=True, *the_rest, **kwargs):
    '''
    A test for commenting on arguments nicely & simply.

    # arg1: string argument for something
    # key: used to auth somewhere
    # *the_rest: list of targets
    # **kwargs: map of locations -> targets
    '''
    pass
