# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os
import sys

from setuptools import setup

from microschema import __version__


if sys.argv[-1] == 'publish':
    os.system('python setup.py register')
    os.system('python setup.py sdist upload')
    os.system('python setup.py bdist_wheel upload --universal')
    sys.exit()


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='microschema',
    version=__version__,
    description='MicroSchema is a schema validation library for Python.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='microschema schema validate validation validator micro',
    url='http://github.com/amibiz/microschema',
    author='Ami E. Bizamcher',
    author_email='ami.bizamcher@gmail.com',
    license='BSD',
    packages=['microschema'],
    test_suite='microschema.tests',
    include_package_data=True,
    zip_safe=False,
)
