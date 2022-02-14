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
        self._id_confing = id_config
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
                if not key and id.match and re.fullmatch(id.match, input):
                    key = id.key
                else:
                    if id_data.getValue(id.key) == "" and not id.optional:
                        ready = False

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

    def get_instructions(self, id_data, rel_path):
        instruction = None
        suites_config = self._id_confing.suites
        if suites_config:
            for choice in suites_config.selector:
                for _id in self._identifiers:
                    if _id.key == choice.id:
                        value = id_data.getValue(_id.key)
                        if re.fullmatch(choice.match, value):
                            if choice.instruction:
                                if choice.instruction.url:
                                    instruction = self.get_instruction_from_url(choice.instruction.url, rel_path)
                                else:
                                    instruction = choice.instruction.text
                            else:
                                instruction = "No instruction found"
                            break
                if instruction:
                    break

        if not instruction:
            instruction = "Press Start to Begin Testing"

        return instruction

    def get_instruction_from_url(self, url , rel_path):
        # Initially support only file read
        file_path = url
        instruction = ""
        if url.startswith(".") and rel_path:
            file_path = os.path.join(url)
        with open(file_path, 'r') as file:
            instruction = file.read()
        return instruction

    instructions = None
