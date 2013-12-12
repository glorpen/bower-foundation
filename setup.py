#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import re
from setuptools import setup
from setuptools.command.build_py import build_py
import imp

here = os.path.dirname(os.path.abspath(__file__))
zurb_pkg = "zurb_foundation"

version = imp.load_source(zurb_pkg, os.path.join(here, 'python', '__init__.py')).__version__

class my_build_py(build_py):
    def _get_data_files(self):
        z = build_py._get_data_files(self)
        
        #add js & css dirs to package
        pkg_dir = os.path.join(self.build_lib, zurb_pkg)
        src_dir = os.path.dirname(self.get_package_dir(zurb_pkg))
        
        for dir in ["scss","js","css"]:
            for root, dirs, files in os.walk(dir):
                z.append((zurb_pkg, os.path.join(src_dir, root), os.path.join(pkg_dir, root), files))
        
        return z

here = os.path.dirname(__file__)
f = open(os.path.join(here, "README.rst"), "rt")
readme = f.read()
f.close()

setup(
    name='zurb-foundation',
    version=version,
    description='The most advanced responsive front-end framework in the world. Quickly create prototypes and production code for sites and apps that work on any kind of device',
    long_description=readme,
    author='ZURB Inc.',
    author_email = "foundation@zurb.com",
    maintainer = "Arkadiusz Dzięgiel",
    maintainer_email = "arkadiusz.dziegiel@glorpen.pl",
    url='http://foundation.zurb.com',
    packages=[zurb_pkg],
    package_dir={zurb_pkg:"python"},
    include_package_data = True,
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
    ],
    cmdclass={'build_py': my_build_py}
)
