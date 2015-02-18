## fake_module

Welcome to the pydocs example.

##### fake_module.args_function

Another example with no-default arguments & some varargs.

```py
args_function(
    arg1,
    arg2
    *args
)
```


##### fake_module.combined_function

A function combining all of the above.

```py
combined_function(
    arg1,
    key=True,
    something='another'
    *the_rest
    **keywords
)
```


##### fake_module.function

An example function.

```py
function()
```


##### fake_module.kwargs_function

A function with keyword arguments & a keywords argument.

```py
kwargs_function(
    key=None,
    something=True
    **kwargs
)
```


##### fake_module.wip_arg_comments

A test for commenting on arguments nicely & simply.

# arg1: string argument for something
# key: used to auth somewhere
# *the_rest: list of targets
# **kwargs: map of locations -> targets

```py
wip_arg_comments(
    arg1,
    key=True
    *the_rest
    **kwargs
)
```
