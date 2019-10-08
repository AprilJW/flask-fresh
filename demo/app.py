from flask import Flask
from . import config

app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER
)
app.config.from_object(config)


def create_app():
    return app


if __name__ == '__main__':
    app.run()
