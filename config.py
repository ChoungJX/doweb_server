import datetime


class index():
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(days=7)
    #PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=10)


    DEBUG = True