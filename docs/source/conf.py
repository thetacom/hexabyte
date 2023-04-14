"""Sphinx Documentation Config."""
project = "hexabyte"  # pylint: disable=invalid-name
copyright = "2023, Justin Cady"  # pylint: disable=invalid-name,redefined-builtin
author = "Justin Cady"  # pylint: disable=invalid-name

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions: list[str] = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.autosummary",
    "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    "sphinx.ext.githubpages",
    "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx-autodoc-typehints",
    "sphinx-git",
    "sphinx-autodoc-annotation",
    "sphinx-rtd-theme",
]

templates_path: list[str] = ["_templates"]
exclude_patterns: list[str] = []

source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "restructuredtext",
    ".md": "markdown",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "alabaster"  # pylint: disable=invalid-name
html_static_path: list[str] = ["_static"]
