# THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
# 
# THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
# DO NOT USE IT IN PRODUCTION.

import logging
import json

_logger = logging.getLogger(__name__)

from .base_node import BaseNode

class StartNode(BaseNode):
    def process(self, params):
        super().process(params)

        parametersJson = {}
        if len(self.definition["parameters"]) > 0:
            parameters = self.definition["parameters"]
            parametersJson = json.loads(parameters)

        return params | parametersJson
