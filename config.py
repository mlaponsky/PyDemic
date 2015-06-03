import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
MONGODB_SETTINGS = {'db': 'PyDemic'}
WTF_CSRF_ENEABLED = True
SECRET_KEY = 'you-will-never-guess'

REDIS_URL = os.environ['REDIS_URL']

FACEBOOK = {'id': '1634720196743881',
            'secret': 'c0127a9cb6c3e73beae751b7d8ff5155',
            'scope': ['email', 'name', 'id']}

GOOGLE = {'id': '371660565684-4jqrhi9bjdci61cvuba1ojm94hb1suao.apps.googleusercontent.com',
          'secret': 'iZ61BbRvU9jQCsY-7AA_EBhV',
          'scope': ['email', 'name', 'id']}
