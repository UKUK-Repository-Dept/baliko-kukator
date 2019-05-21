from flask import Flask
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from views.views import index, build_batches
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import engine
from sqlalchemy import create_engine
from database.db import reflect
from sqlsoup import SQLSoup
from database.dbutils.dbutils import Utils
from configparser import ConfigParser, ExtendedInterpolation

def connect_db(config):
    """
    :param ConfigParser config
    """

    factory = sessionmaker(autocommit=False, autoflush=False)

    db_engine = config.get('database', 'engine')
    username = config.get('database', 'username')
    password = config.get('database', 'password')
    host = config.get('database', 'hostname')
    port = config.get('database', 'port')
    db_name = config.get('database', 'db_name')
    db_url = str(db_engine) + '://' + str(username) + ':' + str(password) + '@' + str(host) + ':' + str(port) + '/' + str(db_name)

    engine = create_engine(db_url)
    session = scoped_session(factory)
    db_meta = reflect(engine)
    db = SQLSoup(db_meta, session=session)

    return db

# read config
conf_file = './config/config.ini'
config = ConfigParser(interpolation=ExtendedInterpolation())
config.read(conf_file)

# create app
viewer = Flask(__name__)
viewer.secret_key = "Super Secret Key"

# connect to DB
db = connect_db(config)

# Instantiate DB utitility class
db_utils = Utils(db)
# Register context processors related to database
db_utils.register_processors(viewer)
    
# create views
admin = Admin(viewer, name="TheProVir - Theses Processing Viewer", 
index_view=AdminIndexView(name="Home", template="index.html", url="/"))

admin.add_view(build_batches(db))

#admin.add_view(batches(name='Batches'))
#admin.add_view(documents(name="Documents"))

# run app
viewer.run()

