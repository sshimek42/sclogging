# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os
import sys

import sphinx_autodoc_typehints
import sphinx_rtd_theme

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
sys.path.insert(0, os.path.abspath("../../src"))
sys.path.append(os.path.abspath("."))
sys.path.append(os.path.abspath("../"))

autodoc_mock_imports = ["coloredlogs", "pyinputplus"]

project = "SCLogging"
copyright = "2022, sshimek42"
author = "sshimek42"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx_rtd_theme",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
]

typehints_fully_qualified = True
always_document_param_types = True

autodoc_typehints = "description"
autodoc_typehints_format = "fully-qualified"
typehints_defaults = "braces"

# napoleon_google_docstring = False
# napoleon_use_param = True
# napoleon_use_ivar = False
# napoleon_numpy_docstring = False
# napoleon_attr_annotations = True
#

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
autosummary_generate = True
