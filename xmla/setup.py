#-*- coding:utf-8 -*-

from setuptools import setup
from distutils.util import get_platform

long_description = open("README.rst").read() + "\n\n" +  open("CHANGES.md").read() 

install_requires=[
    'olap',
    'suds',
    'requests'
    ]

extras_require = {
    "kerberos": ["kerberos"],
    "s4u2p":["s4u2p"]
}

if get_platform().startswith('win'):
    extras_require["sspi"] = ["kerberos-sspi"]
    
# hack, or test wont run on py2.7
try:
    import multiprocessing
    import logging
except:
    pass

setup(
    name='xmla',
    version='0.7.1',
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
    description='Access olap data sources through xmla',
    long_description=long_description,
    author='Norman Krämer',
    author_email='kraemer.norman@googlemail.com',
    packages=['olap', 'olap.xmla'],
    namespace_packages=['olap'],
    package_dir={'olap':'olap', 'olap.xmla': 'olap/xmla'},
    package_data={'olap.xmla': ['vs.wsdl']},
    install_requires=install_requires,
    extras_require = extras_require,
    tests_require = [
        'nose',
        'nose-testconfig',
        'docutils'
    ],

    test_suite = 'nose.collector',

    include_package_data=True,
    zip_safe=False,
)
