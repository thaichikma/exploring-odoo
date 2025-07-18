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
from odoo import tools

from autogen_core import CancellationToken, TRACE_LOGGER_NAME, EVENT_LOGGER_NAME
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent

from autogen_ext.tools.mcp import McpWorkbench

from odoo.addons.nuido_flow.flows.core.base_node import BaseNode
from .utils import process_template, run_async_function

import markdown
from markupsafe import Markup

from .tools import get_chat_completion_client_node, get_tool_nodes, get_mcp_node

autogen_logger = logging.getLogger(TRACE_LOGGER_NAME)
autogen_logger.setLevel(logging.ERROR)
autogen_logger = logging.getLogger(EVENT_LOGGER_NAME)
autogen_logger.setLevel(logging.ERROR)

class AssistantAgentNode(BaseNode):
    def __init__(self, environment, create_function_registry, definitions, definition) -> None:
        super().__init__(environment, create_function_registry, definitions, definition)

        kwargs = self._setup_assistant_agent()

        self.agent = AssistantAgent(**kwargs)

    def _setup_assistant_agent(self):
        completion_node = get_chat_completion_client_node(self)

        self.model_client = completion_node.process({
                "is_structured": self.definition["is_structured"],
                "schema": self.definition["schema"]
            })["client"]

        self.tool_nodes = get_tool_nodes(self)
        self.tools = []
        for tn in self.tool_nodes:
            tools = tn.process({})
            self.tools.extend(tools["tools"])

        self.workbench = None
        self.mcp_server = None
        self.mcp_node = get_mcp_node(self)
        if self.mcp_node is not None:
            self.mcp_server = self.mcp_node.process({})["mcp_server"]
            self.workbench = McpWorkbench(self.mcp_server)

        return {
            'name': "assistant_agent",
            'model_client': self.model_client,
            'system_message': self.definition["system_message"],
            'tools': self.tools,
            'reflect_on_tool_use': self.definition["is_reflect_on_tool_use"],
            'workbench': self.workbench,
        }

    async def _do_ask_ai(self, user_message):
        response = await self.agent.run(task=[TextMessage(content=user_message, source="user")], cancellation_token=CancellationToken())
        return response

    async def _ask_ai(self, params):
        response = TaskResult(messages=[], stop_reason="None")
        try:
            context = self.env.context

            variables = {}
            variables.update(**context)
            variables.update(**params)
            message = process_template(self.definition["prompt"], variables)

            if self.workbench is not None:
                await self.workbench.start()

            response = await self._do_ask_ai(message)
        except:
            _logger.error("Error processing message.", exc_info=True)
            response = TaskResult(messages=[], stop_reason="Error asking AI.")
        finally:
            await self.model_client.close()
            if self.workbench is not None:
                await self.workbench.stop()

        return response

    def process(self, params):
        super().process(params)

        res = run_async_function(self._ask_ai, params)
        result = ""

        message_length = len(res.messages)
        if message_length > 0:
            result = res.messages[len(res.messages) - 1].content

        if self.definition["is_html_result"]:
            result = Markup(tools.html_sanitize(markdown.markdown(result, extensions=['fenced_code', 'sane_lists'])))
        elif self.definition["is_structured"]:
            result = json.loads(result)

        return {
                "result": result
            }
