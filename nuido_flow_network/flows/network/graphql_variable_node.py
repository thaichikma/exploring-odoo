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
from odoo.tools.rendering_tools import parse_inline_template, render_inline_template

from odoo.addons.nuido_flow.flows.core.base_node import BaseNode
from odoo.addons.nuido_flow.flows.tools.tools import get_default_context_for_eval, get_active_record_info

class GraphQlVariableNode(BaseNode):
    def process(self, params) -> any:
        super().process(params)

        context = get_default_context_for_eval(self.env)
        if params is not None:
            context['params'] = params

        info = get_active_record_info(self.env)
        context = {**context, **info}
        res = {}

        try:
            parsed = parse_inline_template(str(self.definition["variables"]))
            res_string = render_inline_template(parsed, context)
            res = json.loads(res_string)
        except:
            _logger.warning("Exception evaluating variables.", exc_info=True)

        return res
