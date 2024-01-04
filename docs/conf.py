import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "Manim Studio"
copyright = "Kovács Bálint-Hunor"
author = "Kovács Bálint-Hunor"
release = "0.1"


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]

# autodoc_mock_imports = ["main", "form_ui"]
intersphinx_mapping = {"python": ("https://docs.python.org/3", None)}
