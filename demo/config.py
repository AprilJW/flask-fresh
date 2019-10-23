import os
from redis import StrictRedis

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASE = {
    'USERNAME': 'root',
    'PASSWORD': 'qwe123',
    'HOST': 'localhost',
    'PORT': 3306,
    'DATABASE': 'flask-env'
}

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}'.format(**DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_TEARDOWN = True

TEMPLATE_FOLDER = os.path.join(BASE_DIR, 'templates')
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

INSTALL_APPS = [
    'apps.user',
    'apps.goods',
    'apps.order',
    'apps.cart',
]

SESSION_TYPE = "redis"
# 设置redis的ip,port,有效时间
REDIS_HOST = "127.0.0.1"
REDIS_PORT = 6379
REDIS_PASSWORD = ''
# 是否强制加盐，混淆session
SESSION_USE_SIGNER = True
# 如果加盐，那么必须设置的安全码，盐
SECRET_KEY = "BjyXUCVnmogYAlBLV9dLxUGK8WtyymyCx1F/E94T//Nf5O4dp2eQjWXnTzyQ4ha1UCo="
# sessons是否长期有效，false，则关闭浏览器，session失效
SESSION_PERMANENT = True
SESSION_REDIS = StrictRedis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

EMAIL_HOST = 'smtp.qq.com'
EMAIL_USER = '919624032@qq.com'
EMAIL_PASS = 'qngkmtqtcakvbgaf'
EMAIL_PORT = 25  #
AUTHORIZATION_CODE = 'hujiakeji2019'
DOMAIN = 'http://127.0.0.1:5000'

LOGIN_URL = '/user/login'

AUTH_USER_MODEL = 'user.User'

FAST_DFS_DOMAIN = 'http://img.summerleaves.cn/'


ALIPAY_APP_ID = '2016101300674998'

APP_PRIVATE_KEY_PATH = os.path.join(BASE_DIR, 'app_private_key.pem')

ALIPAY_PUBLIC_KEY_PATH = os.path.join(BASE_DIR, 'alipay_public_key.pem')