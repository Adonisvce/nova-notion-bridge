import os

def generate_logic_file(logic_name: str, logic_code: str, output_dir="logic"):
    os.makedirs(output_dir, exist_ok=True)
    file_path = os.path.join(output_dir, f"{logic_name}.py")
    with open(file_path, "w") as f:
        f.write(logic_code)
    return file_path
