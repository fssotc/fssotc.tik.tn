#!/usr/bin/env python
import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='mtcfss-website',
    version='0.1',
    description='MTCFSS Website',
    long_description=read('README.md'),
    author='Moez Bouhlel',
    author_email='bmoez.j@gmail.com',
    license='GPLv3',
    url='http://mtcfss.azurewebsites.net/',
    install_requires=[
        'Django'
    ],
    setup_requires=['setuptools_git'],
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.9',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
