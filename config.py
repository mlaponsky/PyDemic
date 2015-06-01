import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
MONGODB_SETTINGS = {'db': 'PyDemic'}
WTF_CSRF_ENEABLED = True
SECRET_KEY = 'you-will-never-guess'

REDIS_URL = "redis://:password@localhost:5000/0"

OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '1634720196743881',
        'secret': 'c0127a9cb6c3e73beae751b7d8ff5155'
    },
    'google': {
        'id': '371660565684-4jqrhi9bjdci61cvuba1ojm94hb1suao.apps.googleusercontent.com',
        'secret': '371660565684-4jqrhi9bjdci61cvuba1ojm94hb1suao@developer.gserviceaccount.com'
    }
}
