from os import environ
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager 
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
login_manager  = LoginManager()

def create_app():
    
    app = Flask(__name__)
    
    CORS(app)

    app.config['SQLALCHEMY_ECHO'] = False
    
    app.config['SECRET_KEY'] = environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DATABASE_URL')
    
    app.config['CORS_HEADERS'] = 'Content-Type'
    
    from .admin import admin_bp
    app.register_blueprint(admin_bp)
    
    from .public import public_bp
    app.register_blueprint(public_bp)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    return app