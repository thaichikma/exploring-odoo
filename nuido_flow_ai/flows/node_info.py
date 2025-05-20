# THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
# 
# THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
# DO NOT USE IT IN PRODUCTION.

from odoo.addons.nuido_flow.flows.node_info import getDefaultInfo

from ..flows.ai.simple_ai_node import SimpleAiNode

def build_simple_ai_node(node, edges):
    info = getDefaultInfo(node, edges)
    info["system_message"] = node["system_message"]
    info["prompt"] = node["prompt"]
    info["is_html_result"] = node["is_html_result"]
    info["is_structured"] = node["is_structured"]
    info["schema"] = node["schema"]

    return info

def create_simple_ai_node(environment, create_function_registry, definitions, definition):
    return SimpleAiNode(environment, create_function_registry, definitions, definition)
