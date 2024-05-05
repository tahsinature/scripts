from typing import List
from getpass import getuser


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


def dict_to_env_semi_colon_seperated(dict: dict) -> str:
    result = ""

    for key, value in dict.items():
        if (not key) or (not value):
            continue
        result += f"{key}={value}; "

    return result.strip()


def dict_to_aws_cred_file(dict: dict):
    required_keys = [
        "aws_access_key_id",
        "aws_secret_access_key",
        "aws_session_token",
        "aws_metadata_user_arn",
    ]

    if not all(key in dict for key in required_keys):
        print(f"missing required keys: {required_keys}")
        return

    content = f"""[default]
aws_access_key_id={dict["aws_access_key_id"]}
aws_secret_access_key={dict["aws_secret_access_key"]}
aws_session_token={dict["aws_session_token"]}
aws_metadata_user_arn={dict["aws_metadata_user_arn"]}
"""
    file_path = f"/Users/{getuser()}/.aws/credentials"

    with open(file_path, "w") as f:
        f.write(content)
