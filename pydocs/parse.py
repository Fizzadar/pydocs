# pydocs
# File: parse.py
# Desc: parse modules & their functions/classes, return markdown templates

from inspect import getmembers, getargspec, isfunction, isclass, ismethod

from .templates import function_template


def _parse_docstring(docstring):
    if docstring is None:
        return None

    docstrings = docstring.split('\n')
    docstrings = [string.strip() for string in docstrings]

    return '\n'.join(docstrings).strip()


def _parse_function(module, name, type, cls=None):
    # Attempt to get decorated function
    if hasattr(type, '__decorated__'):
        type = type.__decorated__

    # Get arguments, build defaults
    argspec = getargspec(type)
    # Make default strings appear as strings
    arg_defaults = [
        "'{}'".format(arg) if isinstance(arg, str) else arg
        for arg in argspec.defaults
    ] if argspec.defaults else None

    # Create a dict of arg name -> default
    defaults = dict(zip(
        argspec.args[-len(arg_defaults):],
        arg_defaults
    )) if arg_defaults else {}

    # Render our function template
    return function_template.render({
        'module': module.__name__,
        'class': cls.__name__ if cls else None,
        'name': name,
        'args': argspec.args,
        'varargs': argspec.varargs,
        'kwargs': argspec.keywords,
        'defaults': defaults,
        'doc_string': _parse_docstring(type.__doc__)
    })

def _parse_class(module, name, type):
    class_attributes = [
        (sub_name, sub_type)
        for (sub_name, sub_type) in getmembers(type)
        if ismethod(sub_type)
        and (
            not getattr(sub_type, '__name__', '_').startswith('_')
            or getattr(sub_type, '__name__', '_') == '__init__'
        )
    ]

    class_docs = [
        _parse_function(module, sub_name, sub_type, cls=type)
        for (sub_name, sub_type) in class_attributes
    ]

    return u'\n'.join(class_docs)

def parse_module(module):
    '''Parse a module's attributes and generate a markdown document.'''
    attributes = [
        (name, type)
        for (name, type) in getmembers(module)
        if (isclass(type) or isfunction(type))
        and type.__module__ == module.__name__
        and not type.__name__.startswith('_')
    ]

    attribute_docs = ['## {}'.format(module.__name__), '']

    if module.__doc__:
        attribute_docs.append(_parse_docstring(module.__doc__))

    for (name, type) in attributes:
        if isfunction(type):
            attribute_docs.append(_parse_function(module, name, type))
        else:
            attribute_docs.append(_parse_class(module, name, type))

    return u'{}\n'.format(
        u'\n'.join(attribute_docs).strip()
    )
