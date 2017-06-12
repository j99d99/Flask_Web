import os

class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'sssxxssxx'

    #UPLOAD_FOLDER = 'server_key'
    #ALLOWED_EXTENSIONS = set(['txt','pdf','jpg'])

    @staticmethod
    def init_app(app):
        pass


class Developmentconfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://mysqlTest:mysqlTest@127.0.0.1/autoinstall'

config = {
    'deveopconfig': Developmentconfig,
    'default': Developmentconfig
}
