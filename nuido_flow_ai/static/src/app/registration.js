// THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
// 
// This software is released under the MIT License.
// https://opensource.org/licenses/MIT
// 
// THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
// DO NOT USE IT IN PRODUCTION.
import { registry } from "@web/core/registry";
import { NuidoNodeRegistryName } from "@nuido/utils/registry";
import { NuidoSidebarMenuItemRegistryName } from "@nuido_base/utils/registry";
import { SimpleAiNode } from "@nuido_flow_ai/components/ai/simple_ai";
import { SimpleAiNodeModel } from "@nuido_flow_ai/models/ai/simple_ai";
// Odoo Nodes
registry.category(NuidoNodeRegistryName).add(SimpleAiNode.name, {
    component: SimpleAiNode,
    model: SimpleAiNodeModel
});
// Menu items
// AI
const aiNodeMenuItemsReg = registry.category(NuidoSidebarMenuItemRegistryName).add("AI", {
    app: "nuidoflow",
    category: "AI",
    items: []
});
const aiNodeMenuItems = aiNodeMenuItemsReg.get("AI");
aiNodeMenuItems.items.push({
    title: "Simple AI",
    icon: "/nuido_flow_ai/static/images/ai.svg",
    type: SimpleAiNode.name
});
