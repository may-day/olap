#-*- coding:utf-8 -*-

from setuptools import setup

long_description = open("README.rst").read() + "\n\n" +  open("CHANGES.md").read() 

install_requires=[
    'olap>=0.3', 'xmla>=0.6', 'pyramid', 'cornice', 'zope.component'
    ]

# hack, or test wont run on py2.7
try:
    import multiprocessing
    import logging
except:
    pass

setup(
    name='olap.rest',
    version='0.1',
    url="https://github.com/may-day/olap",
    license='Apache Software License 2.0',
    classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
        ],
    description='REST access to a pyramid backed olap connection.',
    long_description=long_description,
    author='Norman Krämer',
    author_email='kraemer.norman@googlemail.com',
    packages=['olap', 'olap.rest'],
    namespace_packages=['olap'],
    package_dir={'olap':'olap', 'olap.rest': 'olap/rest'},
    install_requires=install_requires,
    tests_require = [
        'nose',
        'nose-testconfig',
        'docutils'
    ],

    test_suite = 'nose.collector',

    include_package_data=True,
    zip_safe=False,
)
