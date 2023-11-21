from flask import Flask
from .extensions import api, db , migrate, bcrypt, jwt
from .routes import sign_ns
def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config["JWT_SECRET_KEY"] = "secrer-key" 


    api.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    api.add_namespace(sign_ns)




    return app