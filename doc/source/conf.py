# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'doc_example'
copyright = '2024, wgrison'
author = 'wgrison'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'furo'
html_static_path = ['_static']
html_title = "ReLife2" # sidebar title

html_theme_options = {
    "announcement": "<em>beta version</em> ReLife 2 documentation in progress", # annoucement bar
    "light_css_variables": {
        "color-brand-primary": "#7C4DFF",
        "color-brand-content": "#7C4DFF", # color of banner
    },
}

pygments_style = "default" # code color highlight (see from pygments.styles import get_all_styles)
pygments_dark_style = "monokai"  # code color highlight
