# THIS FILE IS A PART OF PUBLIC REPOSITORY https://github.com/yonitjio/exploring-odoo
# 
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT
# 
# THIS SOFTWARE IS EXPERIMENTAL AND FOR EDUCATIONAL PURPOSE ONLY.
# DO NOT USE IT IN PRODUCTION.

from odoo.tools.rendering_tools import parse_inline_template

def process_template(template_txt, variables):
    template = parse_inline_template(str(template_txt))
    result = ""
    renderer = []
    for string, expression, default in template:
        renderer.append(string)
        if expression:
            try:
                value = variables[expression] or default
            except KeyError:
                value = default
            renderer.append(str(value))
    result = ''.join(renderer)
    return result