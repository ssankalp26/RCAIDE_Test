import os
from setuptools import setup

def write_version_py(version, filename="RCAIDE/version.py"):
    content = f"""# THIS FILE IS GENERATED
version = '{version}'
"""
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)

# Define the version
VERSION = "1.0.0"

# Write the version file
write_version_py(VERSION)

# Run setup
setup()
