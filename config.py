# config.py
import os


class Config:
    """基本配置"""
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')

    # 默认的数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:123456@localhost/db1'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CORS_ORIGINS = ["http://127.0.0.1:8000"]  # 前端的域名和端口


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    # 测试环境可以使用 SQLite 或者一个独立的 MySQL 数据库
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///test.db'


class ProductionConfig(Config):
    """生产环境配置"""
    # 生产环境建议从环境变量中读取数据库配置
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# 根据环境变量选择配置
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}