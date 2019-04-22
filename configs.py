import os
import redis


class Config(object):
    Debug = True
    # 项目根目录
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # 模板目录
    TEMPLATES_FOLDER = os.path.join(BASE_DIR, "templates")
    # 静态文件目录
    STATIC_FOLDER = os.path.join(BASE_DIR, "static")
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.61.133:3310/xjzx10'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # redis配置
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 10
    # session
    SECRET_KEY = "python"
    # flask_session的配置信息
    SESSION_TYPE = "redis"  # 指定 session 保存到 redis 中
    SESSION_USE_SIGNER = True  # 让 cookie 中的 session_id 被加密签名处理
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)  # 使用 redis 的实例
    PERMANENT_SESSION_LIFETIME = 60 * 60 * 24 * 14  # session 的有效期，单位是秒


class DevConfig(Config):
    Debug = True
