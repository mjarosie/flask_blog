import os


class Configuration(object):
    APPLICATION_DIR = os.path.dirname(os.path.realpath(__file__))
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}/blog.db'.format(APPLICATION_DIR)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'asjfdasoifsdopfnsafsadfsdofnsd'