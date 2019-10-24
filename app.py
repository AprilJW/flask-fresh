from flask import Flask
import config
from utils.core import DemoInit
from utils.extentions import db, session, admin, csrf

app = Flask(
    __name__,
    template_folder=config.TEMPLATE_FOLDER,
    static_folder=config.STATIC_FOLDER
)

app.config.from_object(config)

demo = DemoInit(app)

extentions = [
    db,
    session,
    admin,
    csrf,
]

application = demo.init(extentions)


@app.template_global('fdfs_img_tag')
def fdfs_img_tag(value):
    return config.FAST_DFS_DOMAIN + value


if __name__ == '__main__':
    app.run()
