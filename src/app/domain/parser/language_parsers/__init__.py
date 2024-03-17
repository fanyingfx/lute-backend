import importlib
import pkgutil
from pathlib import Path

from . import language_parser


def import_submodules() -> None:
    """auto import all submodules
    Because the register_parser() needs the module to be loaded.

    """
    package_dir = Path(__file__).resolve().parent
    for _, module_name, _ in pkgutil.iter_modules([package_dir]):  # type: ignore[list-item]
        full_module_name = f"{__name__}.{module_name}"
        importlib.import_module(full_module_name)


import_submodules()
__all__ = ["language_parser", "parser_helper.py"]
