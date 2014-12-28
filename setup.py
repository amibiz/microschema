# -*- coding: utf-8 -*-
from __future__ import absolute_import

from setuptools import setup

from microschema import __version__

def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='microschema',
    version=__version__,
    description='MicroSchema is a schema validation framework for Python.',
    long_description=readme(),
    classifiers=[
        'Development Status :: 1 - Planning',
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
