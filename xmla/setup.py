#-*- coding:utf-8 -*-

from setuptools import setup
long_description = open("README.txt").read()

setup(
    name='xmla',
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
    description='Access olap data sources through xmla',
    long_description=long_description,
    author='Norman Krämer',
    author_email='kraemer.norman@googlemail.com',
    packages=['olap', 'olap.xmla'],
    namespace_packages=['olap'],
    package_dir={'olap':'olap', 'olap.xmla': 'olap/xmla'},
    package_data={'olap.xmla': ['vs.wsdl']},
    install_requires=[
      'olap == 0.1',
      'suds == 0.4',
      'kerberos == 1.1.1',
      's4u2p == 0.2'
    ],

    include_package_data=True,
    zip_safe=False,
)
