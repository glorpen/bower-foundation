#!/usr/bin/env python

from __future__ import print_function
import os
import re
from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.egg_info import egg_info

here = os.path.dirname(os.path.abspath(__file__))
version_re = re.compile(r'"version"[^"]+"([^"]+)"')
zurb_pkg = "zurb_foundation"

try:
    with open(os.path.join(here, 'bower.json'), "rt") as f:
        version = version_re.search(f.read()).group(1)
except:
    raise Exception("Cannot find version in bower.json")


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
    
    def build_packages(self):
        pkg_dir = self.get_package_dir(zurb_pkg)
        init_py = os.path.join(pkg_dir, "__init__.py")
        #write version
        with open(init_py, "r+t") as f:
            data = f.read().replace("%version%", version)
            f.seek(0)
            f.write(data)
            f.truncate()
        
        build_py.build_packages(self)

setup(
    name='zurb-foundation',
    version=version,
    description='The most advanced responsive front-end framework in the world. Quickly create prototypes and production code for sites and apps that work on any kind of device',
    long_description=
"""
Foundation is the most advanced responsive front-end framework in the world. You can quickly prototype and build sites or apps that work on any kind of device with Foundation, which includes layout constructs (like a fully responsive grid), elements and best practices.
To get started, check out <http://foundation.zurb.com/docs>
""",
    author='ZURB Inc.',
    license='MIT',
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
