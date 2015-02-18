#!/bin/sh

VERSION=`python setup.py --version`

echo "# Releasing pydocs v$VERSION..."

echo "# doing git..."
git tag -a v$VERSION -m v$VERSION
git push --tags

echo "# doing pypi..."
python setup.py sdist upload

echo "# Done!"
