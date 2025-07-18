# THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
# DO NOT USE IT IN PRODUCTION.

import logging

_logger = logging.getLogger(__name__)

import json
from odoo.tools import json_default
from .base_node import BaseNode

class LogNode(BaseNode):
    def process(self, params):
        super().process(params)

        tag = self.definition["tag"]

        log_msg = json.dumps(params, separators=(',', ':'), default=json_default)
        _logger.info("%s: %s", tag, log_msg)

        if "is_debug" in self.env.context and self.env.context["is_debug"]:
            try:
                debug_msg = "Context:  \n```\n" + json.dumps(self.env.context, indent=4, default=json_default) + "  \n```"
                _logger.info("%s: %s", tag + "-debug", debug_msg)
            except Exception as e:
                _logger.info("Unable to log debug message", exc_info=True)

        return params