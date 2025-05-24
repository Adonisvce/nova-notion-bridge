# Contains validation logic for incoming logic payloads
def validate_logic_data(data, schema):
    errors = []
    for field, expected_type in schema.items():
        if field not in data:
            errors.append(f"Missing field: {field}")
        elif not isinstance(data[field], expected_type):
            errors.append(f"Field {field} expected type {expected_type.__name__}, got {type(data[field]).__name__}")
    return errors
