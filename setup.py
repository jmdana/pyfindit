# Copyright (c) 2015 Jose M. Dana
#
# This file is part of pyfindit.
#
# pyfindit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation (version 2 of the License only).
#
# pyfindit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyfindit.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
from setuptools import setup
from setuptools.command.easy_install import easy_install
from setuptools.command.sdist import sdist
import shutil

EXEC_ORIG="pyfindit.py"
EXEC_ORIG_PATH = EXEC_ORIG

EXEC = EXEC_ORIG[:-3]
SCRIPTS_PATH = "scripts"
EXEC_PATH = os.path.join(SCRIPTS_PATH, EXEC)

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

class md_sdist(sdist):
    def run(self):
        # rename the executable
        if not os.path.exists(SCRIPTS_PATH):
            os.makedirs(SCRIPTS_PATH)

        print("Copying %s -> %s" % (EXEC_ORIG_PATH, EXEC_PATH))
        shutil.copyfile(EXEC_ORIG_PATH, EXEC_PATH)
        sdist.run(self)

class md_easy_install(easy_install):
    def run(self):
        easy_install.run(self)
        install_scripts_dest = list(filter(lambda x: x.endswith(EXEC) and "EGG-INFO" not in x,self.outputs))
        install_scripts_dest = os.path.dirname(install_scripts_dest[0]) if len(install_scripts_dest) else os.path.join(sys.prefix,"bin")
        if install_scripts_dest not in os.environ["PATH"]:
            print("\n\n")
            print("*" * 80)
            print("pyfindit has been copied to:\n\n%s\n" % install_scripts_dest)
            print("Which is NOT in your PATH! Please modify your PATH conveniently.")
            print("*" * 80)
            print("\n\n")

setup(
    name="pyfindit",
    version="0.5.9",
    author="Jose M. Dana",
    description=("Smart grep for Python files."),
    license="GNU General Public License v2 (GPLv2)",
    keywords="grep cscope find class def definition initialization python",
    url="https://github.com/jmdana/pyfindit",
    packages=[],
    scripts=[EXEC_PATH],
    cmdclass={
        "easy_install": md_easy_install,
        "sdist": md_sdist,
        },
    zip_safe=False,
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "Topic :: Software Development",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
    ],
    requires=[],
    install_requires=[],
    provides=['pyfindit'],
)


