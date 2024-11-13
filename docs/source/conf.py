# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
# theme used : https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/index.html

import os
import sys

# for local use only
PATH_TO_LIBRARY = "../code/refife"
sys.path.insert(0, os.path.abspath(PATH_TO_LIBRARY))

project = 'doc_example'
copyright = '2024, wgrison'
author = 'wgrison'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # to enable autodoc from docstrings
    "sphinx.ext.napoleon",  # to configure docstring style (use google style by default)
    "sphinx.ext.viewcode",  # to insert source code link next to objects documentation
    "sphinx.ext.githubpages", # necessary to publish to as github pages
    # (see : https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html
    # and https://stackoverflow.com/questions/62626125/github-pages-with-sphinx-generated-documentation-not-displaying-html-correctly)
    "sphinx_copybutton",  # copy button in code block
]
autodoc_typehints = "none"
napoleon_use_rtype = False

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
html_title = "ReLife2"  # sidebar title

html_theme_options = {
    "announcement": "<em>beta version</em> ReLife 2 documentation in progress",  # annoucement bar
}
