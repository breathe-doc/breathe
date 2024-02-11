"""
This script is designed to check that the version numbers that we have in place stay in sync. The
script fails with exit code 1 if they are not the same and always prints the current status.
"""

import sys
import re

import breathe

setup_version = ""
with open("pyproject.toml") as project:
    for line in project:
        if line.startswith("version"):
            match = re.search('"([^"]*)"', line)
            if match:
                setup_version = match.group(1)
                break

if setup_version == breathe.__version__:
    print("Versions match")
    print(f"  {setup_version}")
    print(f"  {breathe.__version__}")
    sys.exit(0)
else:
    print("Versions do not match")
    print(f"  {setup_version}")
    print(f"  {breathe.__version__}")
    sys.exit(1)
