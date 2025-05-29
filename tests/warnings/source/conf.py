# mypy: ignore-errors
from __future__ import annotations

import sys

sys.path.append("../../")

extensions = ["breathe"]

# Breathe configuration parameters
breathe_projects = {
    "class": "../../../examples/doxygen/class/xml/",
    "function": "../../../examples/specific/functionOverload/xml/",
    "group": "../../../examples/specific/group/xml/",
    "invalidproject": "invalid/path/",
}

master_doc = "index"
project = "Test Breathe Warnings"
html_theme = "default"
