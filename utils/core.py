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

    def register_buleprint(self):
        for module in INSTALL_APPS:
            module = '%s.urls' % module
            url = importlib.import_module(module)
            try:
                bule_print = getattr(url, 'blue_print')
            except AttributeError:
                raise AttributeError('you must define your bule_print as "bule_print" name')
            self.app.register_blueprint(bule_print)

    def init(self, *args, **kwargs):
        self.import_modules()
        self.register_buleprint()
        try:
            from . import extentions
        except ImportError as e:
            raise e
