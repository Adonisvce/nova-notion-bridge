import os
from jinja2 import Template

def generate_plugin(plugin_name: str, description: str, input_spec: str, output_spec: str, logic_body: str):
    """Generate a Python plugin file based on input/output spec and logic body."""

    plugin_template = Template("""
"""
Plugin: {{ plugin_name }}
Description: {{ description }}
Input: {{ input_spec }}
Output: {{ output_spec }}
"""

def run(input_data):
    """
    {{ description }}
    """
    {{ logic_body }}
""")

    code = plugin_template.render(
        plugin_name=plugin_name,
        description=description,
        input_spec=input_spec,
        output_spec=output_spec,
        logic_body=logic_body
    )

    plugin_dir = os.path.join("logic_engine", "plugins")
    os.makedirs(plugin_dir, exist_ok=True)

    filename = os.path.join(plugin_dir, f"{plugin_name}.py")
    with open(filename, "w") as f:
        f.write(code)

    print(f"✅ Plugin '{plugin_name}' created at {filename}")

# Example usage (Nova would dynamically trigger this):
# generate_plugin(
#     plugin_name="greet_user",
#     description="Greets the user by name",
#     input_spec="{'name': str}",
#     output_spec="str",
#     logic_body="return f\"Hello, {input_data['name']}!\""
# )
