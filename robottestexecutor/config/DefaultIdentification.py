"""
Copyright (c) 2020- Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
import re
from .IdentificationConfig import IdentifierListSchema
from .IdentificationConfig import default_id_config


class DefaultIdentification:
    def __init__(self, id_list):
        self._identifiers = id_list

    def filter(self, input, id_data):
        key = None
        ready = False
        if input:
            ready = True
            for id in self._identifiers:
                if not key and re.fullmatch(id.match, input):
                    key = id.key
                    if not ready:
                        break
                else:
                    if id_data.getValue(id.key) == "" and not id.optional:
                        ready = False
                        if key:
                            break

        return key, ready
