import subprocess
import re


def get_password(pass_entry, extract_pattern=None):
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
