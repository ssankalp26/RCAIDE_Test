# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
os.environ['SPHINX_BUILD'] = 'sphinx'

# Add all potential module paths
sys.path.insert(0, os.path.abspath('../..'))  # Root directory
sys.path.insert(0, os.path.abspath('../../RCAIDE'))  # RCAIDE directory
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath('.'))))  # Parent of docs

project = 'RCAIDE_LEADS'
copyright = '2024, lab'
author = 'lab'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon'  # Add support for Google/NumPy style docstrings
]

templates_path = ['_templates']
exclude_patterns = []

# Autosummary settings
autosummary_generate = True  # Generate stub pages for autosummary directives
add_module_names = False     # Remove module names from generated documentation

# Mock imports if needed
autodoc_mock_imports = ['Components']  # Add this line to mock the Components module

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


from unittest.mock import Mock

# Mock load_plugin to avoid runtime errors
sys.modules['RCAIDE.Framework.Plugins.load_plugin'] = Mock()

