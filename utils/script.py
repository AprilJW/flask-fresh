import os
from demo import config
from flask_script import Manager
import binascii

manager = Manager()


@manager.option('-n', '--name', dest='app_name')
def startapp(app_name):
    apps = os.path.join(config.BASE_DIR, 'apps')
    init_py = os.path.join(apps, '__init__.py')

    if not os.path.exists(apps):
        os.mkdir(apps)
        init_py = os.path.join(apps, '__init__.py')
        open(init_py, 'w+').close()

    if not os.path.exists(init_py):
        open(init_py, 'w+').close()

    app_path = os.path.join(apps, app_name)

    if os.path.exists(app_path):
        raise Exception('%s app already exist' % app_name)

    os.mkdir(app_path)

    files = [
        '__init__.py',
        'views.py',
        'models.py',
        'urls.py',
        'forms.py',
        'admin.py',
    ]

    current_path = [os.path.join(app_path, file) for file in files]

    _ = lambda file: open(os.path.join(app_path, file), 'w+').close()

    for path in current_path:
        _(path)

    print('%s app create successfully' % app_name)


@manager.command
def createkey():
    random_str = binascii.b2a_base64(os.urandom(50))
    random_str = random_str.decode().strip()
    return random_str
