from typing import List


def get_env_key_value(line: str):
    line = line.strip()
    if not line:
        return None, None

    if "\n" in line:
        raise ValueError("Multiple lines not supported")
    if line.startswith("export "):
        line = line[len("export "):]

    key, value = line.split("=")

    if value.startswith("'") and value.endswith("'"):
        value = value[1:-1]
    elif value.startswith('"') and value.endswith('"'):
        value = value[1:-1]

    return key, value


def get_env_vars_from_lines(lines: str) -> dict:
    env_vars = {}
    lines_array: List[str] = []

    try:
        if "\n" in lines:
            lines_array = lines.split("\n")
        elif ";" in lines:
            lines_array = lines.split(";")
        else:
            lines_array = lines.split("export")

        for line in list(filter(lambda l: l.strip(), lines_array)):
            key, value = get_env_key_value(line.strip())
            env_vars[key] = value
    except Exception as e:
        print(f"""
Invalid Env input: {e}
passed: {lines}
""")

    return env_vars
