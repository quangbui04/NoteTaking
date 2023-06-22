from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Messiisgoat'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views #Import views inside the views file
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note # import models.py here so we can use its functions

    with app.app_context():
        db.create_all()
        print("Create database")
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login' #where should flask redirect us if we are not login
    login_manager.init_app(app) # Tell login manager which app we are using

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # Telling flask how we load a user

    return app
