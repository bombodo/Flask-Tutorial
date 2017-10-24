import os
base_dir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

#cross-site request forgery prevention
WTF_CSRF_ENABLED = True
SECRET_KEY = 'dev key'

SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(base_dir,'app.db') #path of DB file
SQLALCHEMY_MIGRATE_REPO = os.path.join(base_dir,'db_repo') #store migration files
