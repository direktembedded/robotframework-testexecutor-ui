"""
Copyright (c) 2020- Direkt, Australia
Licensed under BSD-3-Clause, refer LICENSE
"""
from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow_dataclass
import marshmallow.validate

# TODO continue to make default behaviour for id list
default_id_config = '''{
    "module": "robottestexecutor.config.DefaultIdentification",
    "implementation": "DefaultIdentification",
    "identifiers": [
                {
                    "key": "device",
                    "name": "Device",
                    "match": "\\\d*"
                },
                {
                    "key": "serial",
                    "name": "Serial No",
                    "match": ".*"
                },
                {
                    "key": "model",
                    "name": "Model",
                    "possibles": ["Simple", "Another", "Super SKU"]
                }
            ]
}
'''


@dataclass
class Identifier:
    key: str = field()
    name: str = field()
    match: Optional[str]
    possibles: List[str] = field(default_factory=list)
    optional: bool = field(default=False)


@dataclass
class IdentifierList:
    module: str = field(default="robottestexecutor.config")
    implementation: str = field(default="DefaultIdentification")
    identifiers: List[Identifier] = field(default_factory=list)


IdentifierListSchema = marshmallow_dataclass.class_schema(IdentifierList)