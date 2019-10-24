import os
from redis import StrictRedis
# import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
# sys.path.insert(0, os.path.join(BASE_DIR, 'utils'))

DATABASE = {
    'USERNAME': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': 3306,
    'DATABASE': 'flask-env'
}

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'.format(**DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

# 注册的app
INSTALL_APPS = [
    'apps.user',
    'apps.goods',
    'apps.order',
    'apps.cart',
]

SESSION_TYPE = "redis"
# 设置redis的ip,port,有效时间
REDIS_HOST = ""
REDIS_PORT = 6379
REDIS_PASSWORD = ''
# 是否强制加盐，混淆session
SESSION_USE_SIGNER = True
# 如果加盐，那么必须设置的安全码，盐
SECRET_KEY = "BjyXUCVnmogYAlBLV9dLxUGK8WtyymyCx1F/E94T//Nf5O4dp2eQjWXnTzyQ4ha1UCo="
# sessons是否长期有效，false，则关闭浏览器，session失效
SESSION_PERMANENT = True
SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

EMAIL_HOST = 'smtp.qq.com'  # smtp.qq.com
EMAIL_USER = ''
EMAIL_PASS = ''
EMAIL_PORT = 25  #
AUTHORIZATION_CODE = ''
DOMAIN = 'http://flask.summerleaves.cn/'  # 项目部署的ip和域名, 本地直接填写http://127.0.0.1:5000

LOGIN_URL = '/user/login'

AUTH_USER_MODEL = 'user.User'  # 用户表

FAST_DFS_DOMAIN = 'http://img.summerleaves.cn/'

ALIPAY_APP_ID = ''   # Alipay的id

APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'app_private_key.pem')

ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'alipay_public_key.pem')
