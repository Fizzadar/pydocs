# pydocs
# File: __init__.py
# Desc: pydocs builds *simple* markdown documentation from your Python files/modules/functions/classes/docstrings

import os
import sys
import json
from importlib import import_module
from os import path, getcwd, chdir, walk, makedirs
from inspect import getmembers, getargspec, isfunction, isclass, ismethod

from jinja2 import Template

from .templates import function_template


_function_template = Template(function_template, trim_blocks=True)

def _parse_function(module, name, type, cls=None):
    # Attempt to get decorated function
    if hasattr(type, '__decorated__'):
        type = type.__decorated__

    # Get arguments, build defaults
    argspec = getargspec(type)
    defaults = dict(zip(argspec.args[-len(argspec.defaults):], argspec.defaults)) if argspec.defaults else {}

    # Render our function template
    return _function_template.render({
        'module': module.__name__,
        'class': cls.__name__ if cls else None,
        'name': name,
        'args': argspec.args,
        'defaults': defaults,
        'doc_string': type.__doc__
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

    attribute_docs = []

    for (name, type) in attributes:
        if isfunction(type):
            attribute_docs.append(_parse_function(module, name, type))
        else:
            attribute_docs.append(_parse_class(module, name, type))

    return u'{}\n'.format(
        u'\n'.join(attribute_docs).strip()
    )


def _parse_module_list(module_list):
    '''Loop through all the modules and parse them.'''
    for module_meta in module_list:
        name = module_meta['module']

        # Import & parse module
        module = import_module(name)
        output = parse_module(module)

        # Assign to meta.content
        module_meta['content'] = output


def _build_module_list(source_module):
    '''Builds a list of python modules in the current directory.'''
    out = []
    dirs_with_init = set()
    module_prefix = '' if source_module == '.' else source_module

    for root, _, filenames in walk('.'):
        root = root[2:]
        module_root = root.replace('/', '.')
        file_names = [filename[:-3] for filename in filenames if filename.endswith('.py')]

        for filename in file_names:
            if filename == '__init__':
                dirs_with_init.add(root)
                module_name = '.'.join([module_prefix, module_root]) if module_root else source_module
            elif not root:
                module_name = '.'.join([module_prefix, filename])
            else:
                module_name = '.'.join([module_prefix, root.replace('/', '.'), filename])

            if module_name.startswith('.'):
                module_name = module_name[1:]

            if root and root not in dirs_with_init:
                print 'No __init__.py, skipping: {}{}.py'.format('{}/'.format(root), filename)
                continue

            source_name = '{}.py'.format(filename)
            if root:
                source_name = '{}/{}'.format(root, source_name)

            if filename == '__init__':
                output_name = 'index.md'
            else:
                output_name = '{}.md'.format(filename)
            if root:
                output_name = '{}/{}'.format(root, output_name)

            out.append({
                'directory': root,
                'file': filename,
                'module': module_name,
                'output': output_name,
                'source': source_name
            })

    return out


def _write_docs(module_list, output_dir):
    '''Write the document meta to our output location.'''
    for module_meta in module_list:
        directory = module_meta['directory']
        # Ensure target directory
        if directory and not path.isdir(directory):
            makedirs(directory)

        # Write the file
        file = open(module_meta['output'], 'w')
        file.write(module_meta['content'])
        file.close()


def build(root, source_module, output_dir, json_dump=False):
    '''Build markdown documentation from a directory and/or python module.'''
    if root.endswith('/'):
        root = root[:-1]

    if output_dir.startswith('/'):
        output_dir = output_dir[1:]

    if not output_dir.endswith('/'):
        output_dir = '{}/'.format(output_dir)

    output_dir = '{}/{}'.format(root, output_dir)

    if source_module == '.':
        source_dir = '{}/'.format(root)
    else:
        source_dir = '{}/{}/'.format(root, source_module.replace('.', os.sep))

    # Cd into the source directory
    chdir(source_dir)
    # And build the module list
    module_list = _build_module_list(source_module)

    # Cd back to old directory
    chdir(root)
    # And parse all the modules
    _parse_module_list(module_list)

    # Cd inot the target directory
    chdir(output_dir)
    # Finally, write the module list to our output dir
    _write_docs(module_list, output_dir)

    if json_dump:
        print json.dumps(module_list, indent=4)


def main():
    '''Main in a function in case you place a build.py for pydocs inside the root directory.'''
    root = getcwd()
    source_module = sys.argv[1]
    output_dir = sys.argv[2]
    json_dump = '--json' in sys.argv
    build(root, source_module, output_dir, json_dump=json_dump)
