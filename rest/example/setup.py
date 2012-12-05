#-*- coding:utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
    name = "olaprest-example",
    version = "0.1",
    maintainer = "Norman Krämer",
    maintainer_email = "kraemer.norman@gmail.com",
    description = "OLAP REST Service example",
    long_description = "A mini pyramid application serving 2 olap connection via REST",
    url = "https://github.com/may-day/olap/tree/master/rest/example",
    license='Apache Software License 2.0',
    keywords = ['olap', 'REST', 'pyramid', 'example'],
    classifiers = [
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 2",
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],    
    install_requires=[
        'olap', 'xmla', 'pyramid', 'cornice', 'zope.component'
    ],
    entry_points = {
      'console_scripts': [
        'olaprestexample = mini:main',
      ],
    },
    py_modules = ['mini'],

)

