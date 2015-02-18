# pydocs
# File: __init__.py
# Desc: pydocs builds *simple* markdown documentation
#       uses your Python files/modules/functions/classes/docstrings

import os
import sys
import json
from importlib import import_module
from os import path, getcwd, chdir, walk, makedirs

from .parse import parse_module


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

    # Ensure output_dir format (no / at start, / at end)
    if output_dir.startswith('/'):
        output_dir = output_dir[1:]

    if not output_dir.endswith('/'):
        output_dir = '{}/'.format(output_dir)

    # Apply root to it, make the directory if not exists
    output_dir = '{}/{}'.format(root, output_dir)
    if not path.isdir(output_dir):
            makedirs(output_dir)

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
