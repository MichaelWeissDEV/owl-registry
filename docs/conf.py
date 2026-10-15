"""Sphinx configuration for the owl-registry documentation."""

from __future__ import annotations

project = "OWL Registry"
author = "Michael Weiss"
copyright = "2026, Michael Weiss"  # noqa: A001
release = "alpha"
version = release

extensions = [
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinxcontrib.mermaid",
]

myst_enable_extensions = ["colon_fence", "deflist", "fieldlist", "attrs_inline", "tasklist"]
myst_heading_anchors = 3

source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
master_doc = "index"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store", "requirements.txt"]

html_theme = "furo"
html_title = "OWL Registry"
html_logo = "_static/owl.png"
html_favicon = "_static/favicon.png"
html_static_path = ["_static"]
html_theme_options = {
    "source_repository": "https://github.com/MichaelWeissDEV/owl-registry/",
    "source_branch": "main",
    "source_directory": "docs/",
}
copybutton_prompt_text = r"^\$ |^>>> "
copybutton_prompt_is_regexp = True
