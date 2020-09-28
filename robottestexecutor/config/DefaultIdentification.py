"""
Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
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
