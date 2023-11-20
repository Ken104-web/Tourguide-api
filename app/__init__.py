from flask import Flask
from .extensions import api, db , migrate

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'


    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)



    return app