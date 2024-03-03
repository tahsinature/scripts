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

    try:
        if "\n" in lines:
            lines = lines.split("\n")
        elif ";" in lines:
            lines = lines.split(";")
        else:
            lines = lines.split("export")

        for line in lines:
            key, value = get_env_key_value(line.strip())
            env_vars[key] = value
    except Exception as e:
        print(f"""
Invalid Env input: {e}
passed: {lines}
""")

    return env_vars
