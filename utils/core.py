import importlib


def import_modules():
    from demo.config import INSTALL_APPS
    for module in INSTALL_APPS:
        module = '%s.models' % module
        importlib.import_module(module)
