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
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",  # to insert source code link next to objects documentation
    "sphinx.ext.githubpages", # necessary to publish to as github pages
    # (see : https://www.sphinx-doc.org/en/master/usage/extensions/githubpages.html
    # and https://stackoverflow.com/questions/62626125/github-pages-with-sphinx-generated-documentation-not-displaying-html-correctly)
    "sphinx_copybutton",  # copy button in code block
    "numpydoc", # if used, get rid of napoleon
]

autodoc_typehints = "none"
# autosummary_generate = True

# napoleon_use_param = False
# napoleon_use_rtype = False
autodoc_class_signature = "separated" # remove Class(*args, **kwargs)

# copied from sklearn
#########################################################################################
# We do not need the table of class members because `sphinxext/override_pst_pagetoc.py`
# will show them in the secondary sidebar
numpydoc_show_class_members = False
numpydoc_show_inherited_class_members = False
# We want in-page toc of class members instead of a separate page for each entry
numpydoc_class_members_toctree = False


# For maths, use mathjax by default and svg if NO_MATHJAX env variable is set
# (useful for viewing the doc offline)
if os.environ.get("NO_MATHJAX"):
    extensions.append("sphinx.ext.imgmath")
    imgmath_image_format = "svg"
    mathjax_path = ""
else:
    extensions.append("sphinx.ext.mathjax")
    mathjax_path = "https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"
#########################################################################################

templates_path = ['_templates', '_templates/autosummary']
# exclude_patterns = ['_build', '_templates'] # note to be parsed by compiler

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_static_path = ['_static']
html_title = "ReLife2"  # sidebar title

html_theme_options = {
    "announcement": "<em>beta version</em> ReLife 2 documentation in progress",  # annoucement bar
    "navigation_with_keys" : False,
}
