#  Copyright 2021 Direkt Embedded Pty Ltd
#  Copyright (c) 2020 Sipke Vriend
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

import re
import os
from testexecutor.model.KeyValueModel import KeyValue


class DefaultIdentification:
    def __init__(self, id_config, id_data):
        self._identifiers = id_config.identifiers
        for id in self._identifiers:
            id_data.add(id.key, KeyValue(id.name, ""), id.possibles)

    def filter(self, input, id_data):
        key = None
        ready = False
        if input:
            ready = True
            for id in self._identifiers:
                if id.possibles and not id_data.getValue(id.key):
                    id_data.setPossibleValues(id.key, id.possibles)
                if not key and re.fullmatch(id.match, input):
                    key = id.key
                else:
                    if id_data.getValue(id.key) == "" and not id.optional:
                        ready = False

        if ready:
            self.instructions = "Press Start to begin testing"

        return key, ready

    def get_suite(self, suites_config, id_data):
        suite = None
        if suites_config:
            for choice in suites_config.selector:
                for _id in self._identifiers:
                    if _id.key == choice.id:
                        value = id_data.getValue(_id.key)
                        if re.fullmatch(choice.match, value):
                            suite = os.path.join(suites_config.path, choice.suite)
                            break
                if suite:
                    break

        return suite

    instructions = None
