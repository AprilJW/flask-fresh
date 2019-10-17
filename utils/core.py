import importlib
from demo.config import INSTALL_APPS


class DemoInit(object):
    def __init__(self, app):
        self.app = app

    @staticmethod
    def import_modules():
        for module in INSTALL_APPS:
            module = '%s.models' % module
            importlib.import_module(module)

    def register_blue_print(self):
        for module in INSTALL_APPS:
            module = '%s.urls' % module
            url = importlib.import_module(module)
            try:
                blue_print = getattr(url, 'blue_print')
            except AttributeError:
                raise AttributeError('you must define your blue_print as "blue_print" name')
            self.app.register_blueprint(blue_print)

    def initialize_admin(self):
        for module in INSTALL_APPS:
            module = '%s.admin' % module
            importlib.import_module(module)

    def init(self, *args, **kwargs):
        self.import_modules()
        self.register_blue_print()
        self.initialize_admin()
        try:
            from . import extentions
        except ImportError as e:
            raise e
