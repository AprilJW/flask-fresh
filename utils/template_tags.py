from demo.app import create_app
from demo.config import FAST_DFS_DOMAIN

app = create_app()


@app.template_global('fdfs_img_tag')
def fdfs_img_tag(value):
    return FAST_DFS_DOMAIN + value
