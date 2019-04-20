class Config(object):
    Debug = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:123456@192.168.61.132:3310/xjzx10'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig(Config):
    Debug = True
