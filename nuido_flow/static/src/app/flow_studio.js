// THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
// 
// THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
// DO NOT USE IT IN PRODUCTION.
import { registry } from "@web/core/registry";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { standardActionServiceProps } from "@web/webclient/actions/action_service";
import { rpc } from "@web/core/network/rpc";
import { NuidoStudio } from "@nuido_base/app/studio";
import { HorizontalOrthoEdge, VerticalOrthoEdge } from "@nuido_base/components/edges/orthogonal_edge";
class NuidoFlowStudio extends NuidoStudio {
    async onBeforeShowChatDialog() {
        await this.onSave();
    }
    get appName() {
        return "nuidoflow";
    }
    get edgeType() {
        return HorizontalOrthoEdge.name;
    }
    get auxEdgeType() {
        return VerticalOrthoEdge.name;
    }
    onAfterSave(newId) {
        window.location.assign(("/odoo/nuidoflow/" + newId + "/NuidoFlowStudio"));
    }
    clearCaches() {
        const hasStarterNode = this.currentDoc.nodes.findIndex(o => o.nodeType.endsWith("StarterNode")) > -1;
        if (hasStarterNode) {
            this.env.bus.trigger("CLEAR-CACHES");
        }
    }
    async onSave() {
        const isProcessed = this.currentDoc.isProcessed;
        let confirmed = false;
        if (isProcessed) {
            confirmed = await new Promise((resolve) => {
                this.dialog.add(ConfirmationDialog, {
                    title: 'Confirmation',
                    body: "The flow is already processed, continuing will reset it. Proceed?",
                    confirm: () => resolve(true),
                    cancel: () => resolve(false),
                });
            });
        }
        if (confirmed || !isProcessed) {
            this.clearCaches();
            await super.onSave();
            this.currentDoc.isProcessed = false;
        }
    }
    async onProcessButtonClick() {
        let confirmed = false;
        if (!this.props.action.context.active_id) {
            await new Promise((resolve) => {
                this.dialog.add(ConfirmationDialog, {
                    title: 'Error',
                    body: "Can not run unsaved flow.",
                });
            });
            return;
        }
        const hasTriggerNode = this.currentDoc.nodes.findIndex(o => o.nodeType.endsWith("TriggerNode")) > -1;
        confirmed = false;
        if (hasTriggerNode) {
            confirmed = await new Promise((resolve) => {
                this.dialog.add(ConfirmationDialog, {
                    title: 'Confirmation',
                    body: "Processing the flow will register trigger nodes into Odoo system. Proceed?",
                    confirm: () => resolve(true),
                    cancel: () => resolve(false),
                });
            });
        }
        if (confirmed || !hasTriggerNode) {
            this.clearCaches();
            const res = await rpc("/nuidoflow/process", {
                "def_id": this.props.action.context.active_id,
            });
            this.currentDoc.isProcessed = true;
            return res;
        }
        return false;
    }
    async onRunButtonClick() {
        let confirmed = false;
        if (!this.props.action.context.active_id) {
            await new Promise((resolve) => {
                this.dialog.add(ConfirmationDialog, {
                    title: 'Error',
                    body: "Can not run unsaved flow.",
                });
            });
            return;
        }
        const isProcessed = this.currentDoc.isProcessed;
        confirmed = false;
        if (!isProcessed) {
            confirmed = await new Promise((resolve) => {
                this.dialog.add(ConfirmationDialog, {
                    title: 'Confirmation',
                    body: "Running the flow will process it first. Proceed?",
                    confirm: () => resolve(true),
                    cancel: () => resolve(false),
                });
            });
        }
        else {
            confirmed = true;
        }
        if (confirmed) {
            this.clearCaches();
            const res = await rpc("/nuidoflow/run", {
                "def_id": this.props.action.context.active_id,
            });
            this.currentDoc.isProcessed = true;
            return res;
        }
        return false;
    }
}
NuidoFlowStudio.res_model = "nuido_flow.node.definition";
NuidoFlowStudio.template = "nuido_flow.flow-studio";
NuidoFlowStudio.components = {
    ...NuidoStudio.components
};
NuidoFlowStudio.props = {
    ...standardActionServiceProps,
};
registry.category("actions").add("NuidoFlowStudio", NuidoFlowStudio);
