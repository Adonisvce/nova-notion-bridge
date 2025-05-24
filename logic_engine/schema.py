# Defines schemas for logic validation or Notion structure
def get_expected_logic_schema():
    return {
        "name": str,
        "description": str,
        "trigger": str,
        "actions": list,
    }
