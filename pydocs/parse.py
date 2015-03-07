# pydocs
# File: parse.py
# Desc: parse modules & their functions/classes, return markdown templates

import re
from inspect import getmembers, getargspec, isfunction, isclass, ismethod

from .templates import function_template


ARG_COMMENT_REGEX = r'# ([a-zA-Z0-9_\*]+): (.*)'

def _parse_docstring(docstring):
    if docstring is None:
        return None, {}

    docstrings = [string.strip() for string in docstring.split('\n')]

    outputs = []
    arg_comments = {}

    for line in docstrings:
        matches = re.search(ARG_COMMENT_REGEX, line)
        if matches:
            arg_comments[matches.group(1)] = matches.group(2)
        else:
            outputs.append(line)

    return '\n'.join(outputs).strip(), arg_comments


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

    docstring, arg_comments = _parse_docstring(type.__doc__)

    # Render our function template
    return function_template.render({
        'module': module.__name__,
        'class': cls.__name__ if cls else None,
        'name': name,
        'args': argspec.args,
        'varargs': '*{}'.format(argspec.varargs),
        'kwargs': '**{}'.format(argspec.keywords),
        'defaults': defaults,
        'doc_string': docstring,
        'arg_comments': arg_comments
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
        docstring, _ = _parse_docstring(module.__doc__)
        attribute_docs.append(docstring)

    for (name, type) in attributes:
        if isfunction(type):
            attribute_docs.append(_parse_function(module, name, type))
        else:
            attribute_docs.append(_parse_class(module, name, type))

    return u'{}\n'.format(
        u'\n'.join(attribute_docs).strip()
    )
