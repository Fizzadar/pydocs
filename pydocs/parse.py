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


def _parse_function(module, name, type_, cls=None):
    # Attempt to get decorated function
    if hasattr(type_, '__decorated__'):
        type_ = type_.__decorated__

    # Get arguments, build defaults
    argspec = getargspec(type_)
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

    docstring, arg_comments = _parse_docstring(type_.__doc__)

    # Render our function template
    return function_template.render({
        'module': module.__name__,
        'class': cls.__name__ if cls else None,
        'name': name,
        'args': argspec.args,
        'varargs': '*{}'.format(argspec.varargs) if argspec.varargs else None,
        'kwargs': '**{}'.format(argspec.keywords) if argspec.keywords else None,
        'defaults': defaults,
        'doc_string': docstring,
        'arg_comments': arg_comments
    })


def _parse_class(module, name, type_):
    class_attributes = [
        (sub_name, sub_type)
        for (sub_name, sub_type) in getmembers(type_)
        if ismethod(sub_type)
        and (
            not getattr(sub_type, '__name__', '_').startswith('_')
            or getattr(sub_type, '__name__', '_') == '__init__'
        )
    ]

    class_docs = [
        _parse_function(module, sub_name, sub_type, cls=type_)
        for (sub_name, sub_type) in class_attributes
    ]

    return u'\n'.join(class_docs)


def parse_module(module):
    '''Parse a module's attributes and generate a markdown document.'''
    attributes = [
        (name, type_)
        for (name, type_) in getmembers(module)
        if (isclass(type_) or isfunction(type_))
        and type_.__module__ == module.__name__
        and not type_.__name__.startswith('_')
    ]

    attribute_docs = ['## {0}'.format(module.__name__), '']

    if module.__doc__:
        docstring, _ = _parse_docstring(module.__doc__)
        attribute_docs.append(docstring)

    if hasattr(module, '__all__'):
        for name in module.__all__:
            link = '+ [{0}](./{0}.md)'.format(name)
            attribute_docs.append(link)

    for (name, type_) in attributes:
        if isfunction(type_):
            attribute_docs.append(_parse_function(module, name, type_))
        else:
            attribute_docs.append(_parse_class(module, name, type_))

    return u'{0}\n'.format(
        u'\n'.join(attribute_docs).strip()
    )
