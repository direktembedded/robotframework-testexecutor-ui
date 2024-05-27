#!/usr/bin/env python3
#  Copyright 2022 Direkt Embedded Pty Ltd
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
A module used to package a version of the python package as defined by setup.py which should be in the same
directory as this file.
git describe --dirty is used to check that the VERSION content is the same, to ensure a packages isn't created
which does not match the git tag. It also does not allow for a package to be created if the git tree is dirty.
"""

packagename='robottestexecutor'


def getGitVersion():
    import subprocess
    return subprocess.check_output(["git", "describe", "--dirty"]).strip().decode()


def isVersionClean(version):
    return not ('dirty' in version)


def package():
    from build.__main__ import main
    print("VERSION file matches git version, running setup to package")
    main(["--sdist", "--wheel"])


if __name__ == "__main__":
    import os
    return_code = -1
    current_path = os.path.dirname(os.path.abspath(__file__))
    package_path = os.path.join(current_path, packagename)
    version = getGitVersion()
    if isVersionClean(version):
        with open(os.path.join(package_path, 'VERSION'), "r") as version_file:
            fileVersion = version_file.read().strip()
        if fileVersion != version:
            with open(os.path.join(package_path, 'VERSION'), "w") as version_file:
                print(version, file=version_file)
                print("File version ({0}) not same as git version ({1})\nFile has been updated\nPlease confirm, commit, tag and re-run this script".format(fileVersion, version))
        else:
            package()
    else:
        print("Git version ({0}) not clean, not packaging\ngit tree must be clean and tag must match VERSION file".format(version))

    exit(0)
