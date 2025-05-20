# THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
# 
# THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
# DO NOT USE IT IN PRODUCTION.

import json

from odoo import tools

from autogen_core import CancellationToken
from autogen_core.models import ModelInfo
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient

from odoo.addons.nuido_flow.flows.core.base_node import BaseNode
from .utils import process_template
from ...ai import async_utils

import markdown
from markupsafe import Markup

from pydantic import BaseModel, Field

class AgentResponse(BaseModel):
    id: int
    label: str = Field(..., description="A label related to the id, can be name, description, or any value asked by user.")

class SimpleAiNode(BaseNode):
    def __init__(self, environment, create_function_registry, definitions, definition) -> None:
        super().__init__(environment, create_function_registry, definitions, definition)


        # response_format = { "type": "text" }
        if self.definition["is_structured"]:
            response_format = {
                    "type": "json_schema",
                    "json_schema": {
                        "name": "structured_output",
                        "description": "Your reply.",
                        "schema": json.loads(self.definition["schema"]),
                    }
                }

            self.model_client = OpenAIChatCompletionClient(
                model="gemma-3-4b-it",
                api_key="__NOT_USED__",
                base_url="http://192.168.56.1:1234/v1",
                model_info=ModelInfo(family="unknown", function_calling=True, json_output=True, vision=True, structured_output=True ),
                response_format=response_format
            )
        else:
            self.model_client = OpenAIChatCompletionClient(
                model="gemma-3-4b-it",
                api_key="__NOT_USED__",
                base_url="http://192.168.56.1:1234/v1",
                model_info=ModelInfo(family="unknown", function_calling=True, json_output=True, vision=True, structured_output=True ),
            )

        self.agent = AssistantAgent(
            name="simple_agent",
            model_client=self.model_client,
            system_message=definition["system_message"]
        )

    async def _ask_ai(self, params):
        variables = {}
        variables.update(**self.env.context)
        variables.update(**params)
        msg = process_template(self.definition["prompt"], variables)

        response = await self.agent.on_messages([TextMessage(content=msg, source="user")], cancellation_token=CancellationToken())
        return response


    def process(self, params):
        super().process(params)

        res = async_utils.run_async_function(self._ask_ai, params)
        result = res.chat_message.content

        if self.definition["is_html_result"]:
            result = Markup(tools.html_sanitize(markdown.markdown(result, extensions=['fenced_code', 'sane_lists'])))

        return {
                "result": result
            }
