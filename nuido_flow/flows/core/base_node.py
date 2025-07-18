# THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
#
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
#
# THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
# DO NOT USE IT IN PRODUCTION.

import typing
from typing_extensions import Protocol

from odoo.api import Environment

@typing.runtime_checkable
class FlowNode(Protocol):
    def process(self, params) -> any:
        ...

    def get_next_node_info(self) -> dict | None:
        ...


class BaseNode(FlowNode):
    """
    Base class for all nodes in the flow.

    Args:
        environment (Environment): The Odoo environment.
        create_function_registry (CreateFunctionRegistry): The registry of functions for creating nodes.
        definitions (dict): The definitions of the nodes in the flow.
        definition (dict): The definition of this node.

    """
    def __init__(self, environment, create_function_registry, definitions, definition) -> None:
        self.next_node_info = None
        self.env: Environment = environment
        self.create_function_registry = create_function_registry
        self.definitions = definitions
        self.definition = definition

        self.id = self.definition["id"]


    def process(self, params) -> any:
        if "next_nodes" in self.definition and len(self.definition["next_nodes"]) > 0:
            self.next_node_info = self.definition["next_nodes"][0]
        else:
            self.next_node_info = None

        return params

    def get_next_node_info(self):
        return self.next_node_info
