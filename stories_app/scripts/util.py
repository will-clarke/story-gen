import subprocess
import re
import os


def get_password(envvar: str, pass_entry: str, extract_pattern=None):
    if envvar in os.environ:
        return os.environ[envvar]
    try:
        password = subprocess.check_output(
            ["pass", pass_entry], universal_newlines=True
        ).strip()

        if extract_pattern:
            match = re.search(extract_pattern, password)
            if match:
                return match.group(1)

        return password
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None
