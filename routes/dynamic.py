from flask import Blueprint, request, jsonify

dynamic_bp = Blueprint("dynamic", __name__)

@dynamic_bp.route("/dynamic", methods=["POST"])
def handle_dynamic_logic():
    try:
        data = request.get_json()

        # Expecting a payload like:
        # {
        #     "logic_name": "greet_user",
        #     "input": {
        #         "name": "Thomas"
        #     }
        # }

        logic_name = data.get("logic_name")
        input_data = data.get("input", {})

        # Basic demo logic map
        def greet_user(name):
            return f"Hello, {name}! Nova is online and listening."

        # Logic map
        logic_map = {
            "greet_user": lambda: greet_user(input_data.get("name", "friend")),
            # Add more logic entries here
        }

        if logic_name not in logic_map:
            return jsonify({"error": f"Logic '{logic_name}' not found"}), 400

        result = logic_map[logic_name]()
        return jsonify({"result": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
