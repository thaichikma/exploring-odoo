// THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
// 
// THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
// DO NOT USE IT IN PRODUCTION.
import { Node } from "@nuido/components/node";
import { TextDialogInput } from "@nuido_base/components/dialogs/text_dialog_input";
export class SimpleAiNode extends Node {
    onPromptChanged(value) {
        this.props.node.prompt = value;
    }
    onSystemMessageChanged(value) {
        this.props.node.system_message = value;
    }
    onIsStructuredOutputChanged(event) {
        if (!this.props.node.is_structured) {
            this.props.node.is_structured = true;
        }
        else {
            this.props.node.is_structured = false;
        }
        this.refreshEdges();
        this.props.node.schema = "";
    }
    onIsHtmlResultChanged(event) {
        if (!this.props.node.is_html_result) {
            this.props.node.is_html_result = true;
        }
        else {
            this.props.node.is_html_result = false;
        }
    }
    onSchemaChanged(value) {
        this.props.node.schema = value;
    }
    get isHtmlResultId() {
        return `input-${this.props.node.id}-is-html-result`;
    }
    get isStructuredInputId() {
        return `input-${this.props.node.id}-is-structured-output`;
    }
}
SimpleAiNode.template = "nuido_flow_sales.simple-ai";
SimpleAiNode.components = {
    ...Node.components,
    TextDialogInput
};
