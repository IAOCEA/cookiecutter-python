from importlib.metadata import version

try:
    __version__ = version("{{ cookiecutter.project_slug }}")
except Exception:
    __version__ = "999"
