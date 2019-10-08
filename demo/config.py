import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = {
    'USERNAME': 'root',
    'PASSWORD': 'qwe123',
    'HOST': 'localhost',
    'PORT': 3306,
    'DATABASE': 'flask-env'
}

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'.format(**DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

INSTALL_APPS = [
    # 'apps.user'
]
