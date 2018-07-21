# 配置基类
import os

class BaseConfig():
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '!@#$%^&*DGHJKL%^&*(CVBERTYU1231'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, 'myApp/static/img/')

# 开发环境
class DevelopConfig(BaseConfig):
    DEBUG = True
    MAIL_SERVER = "smtp.163.com"
    MAIL_USERNAME = "small_pupil@163.com"
    MAIL_PASSWORD = "shangxin1010"

    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sql_exam.db')

# 测试环境
class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sql_exam.db')

# 演示环境
class StagingConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sql_exam.db')

# 线上环境
class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'sql_exam.db')

config = {
    'develop': DevelopConfig,
    'testing': TestingConfig,
    'staging': StagingConfig,
    'product': ProductConfig,
    'default': DevelopConfig
}