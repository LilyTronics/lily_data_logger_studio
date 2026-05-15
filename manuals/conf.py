"""
Configuration file for the Sphinx documentation builder.

For the full list of built-in configuration values, see the documentation:
https://www.sphinx-doc.org/en/master/usage/configuration.html

-- Project information -----------------------------------------------------
https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
"""

# Disable message for naming convention in this file,
# because we must comply to the sphinx naming convention
# pylint: disable=invalid-name
# pylint: disable=redefined-builtin

import os
import sys

from datetime import date

import src.app_data as AppData


source_path = os.path.abspath(os.path.join(
    os.path.dirname(__file__),
    '..',
    'instruments'
))
sys.path.insert(0, source_path)

project = AppData.APP_NAME
copyright = f"{date.today().year} {AppData.COMPANY}"
author = AppData.COMPANY
release = f"V{AppData.VERSION}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration
extensions = [
    'sphinx.ext.autodoc'
]
autodoc_member_order = 'bysource'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_logo = ''
html_favicon = ''
html_copy_source = False
html_show_sourcelink = False
html_show_sphinx = False

html_theme_options = {
    "collapse_navigation": False,
}
