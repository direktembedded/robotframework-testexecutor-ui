#!/usr/bin/env python3
#  Copyright 2023 Direkt Embedded Pty Ltd
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

"""
Pip setup file used to create a package for robot-testexecutor.
"""

import setuptools
import os

current_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(current_path, 'robottestexecutor', 'VERSION')) as version_file:
    VERSION = version_file.read().strip()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="robotframework-testexecutor-ui",
    version=VERSION,
    description="This module is a library which provides a test runner using Robot Framework and controller using Test Executor™. TestArchiver ArchiverRobotListener can be used to archive the test results.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    package_data={'robotframework-testexecutor-ui': ['VERSION']},
    url="https://www.direktembedded.com",
    license_files=("LICENSE", "NOTICE"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache-2.0",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'testexecutor-ui>=0.6',
        'marshmallow_dataclass>=8.5.8',
        'psycopg2-binary>=2.9.3',
        'robotframework>=4.1.3'
    ],
    extras_require={
        'archiver': 'testarchiver>=2.6.1'
    },
    python_requires='>=3.6',
)

# python -m pip install --user --upgrade setuptools wheel
# python setup.py sdist bdist_wheel
