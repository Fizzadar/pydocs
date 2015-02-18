# pydocs
# File: setup.py
# Desc: needed

from setuptools import setup


if __name__ == '__main__':
    setup(
        version='0.1',
        name='pydocs',
        description='Auto generate markdown documents with Python.',
        author='Nick @ Oxygem',
        author_email='nick@oxygem.com',
        url='http://github.com/Fizzadar/pydocs',
        package_dir={
            'pydocs': 'pydocs'
        },
        scripts=[
            'bin/pydocs'
        ],
        install_requires=[
            'jinja2>=2',
            'docopt>=0.6'
        ]
    )
