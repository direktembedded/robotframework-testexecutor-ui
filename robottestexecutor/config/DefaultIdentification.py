"""
Copyright (c) 2020- Sipke Vriend
Licensed under BSD-3-Clause, refer LICENSE
"""
import re
from testexecutor.model.KeyValueModel import KeyValue


class DefaultIdentification:
    def __init__(self, id_list, id_data):
        self._identifiers = id_list
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

    instructions = None
