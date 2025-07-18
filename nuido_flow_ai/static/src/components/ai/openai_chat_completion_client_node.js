// THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
// 
// THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
// DO NOT USE IT IN PRODUCTION.
import { Node } from "@nuido/components/node";
import { TextInputDialogInput } from "@nuido_base/components/dialogs/text_input_dialog_input";
export class OpenAiChatCompletionClientNode extends Node {
    onAiModelChanged(event) {
        this.props.node.model = event.target.value;
    }
    onApiKeyChanged(value) {
        this.props.node.api_key = value;
    }
    onBaseUrlChanged(value) {
        this.props.node.base_url = value;
    }
    get aiModelInputId() {
        return `input-${this.props.node.id}-ai-model`;
    }
}
OpenAiChatCompletionClientNode.template = "nuido_flow_ai.openai-chat-completion-client-node";
OpenAiChatCompletionClientNode.components = {
    ...Node.components,
    TextInputDialogInput
};
