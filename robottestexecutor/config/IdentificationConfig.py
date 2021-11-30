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

from dataclasses import dataclass, field
from typing import List, Optional

import marshmallow_dataclass
import marshmallow.validate

# TODO add a directory path so user can specify it be added to python module path
default_id_config = '''{
    "module": "robottestexecutor.config.DefaultIdentification",
    "implementation": "DefaultIdentification",
    "identifiers": [
                {
                    "key": "serial",
                    "name": "Serial No",
                    "match": "\\\d*"
                },
                {
                    "key": "info",
                    "name": "Info",
                    "match": ".*"
                },
                {
                    "key": "model",
                    "name": "Model",
                    "possibles": ["ModelA", "ModelB", "ModelC"]
                }
            ],
    "suites": { 
            "path": "./models",
            "selector": [
                {
                    "id": "model",
                    "match": "ModelA.*",
                    "suite": "ModelA-Suite.robot"
                },
                {
                    "id": "model",
                    "match": "ModelB",
                    "suite": "ModelB-Suite.robot"
                },
                {
                    "id": "model",
                    "match": "ModelC.*",
                    "suite": "ModelC-Suite.robot"
                }
            ]
        }
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
class SuiteSelector:
    id: str = field()
    match: str = field()
    suite: Optional[str]


@dataclass
class SuiteInfo:
    path: str = field(default=".")
    selector: List[SuiteSelector] = field(default_factory=list)


@dataclass
class IdentifierConfig:
    suites: SuiteInfo = field()
    module: str = field(default="robottestexecutor.config.DefaultIdentification")
    implementation: str = field(default="DefaultIdentification")
    identifiers: List[Identifier] = field(default_factory=list)


IdentifierListSchema = marshmallow_dataclass.class_schema(IdentifierConfig)
