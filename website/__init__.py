from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

# Configure the database and initialize it
db = SQLAlchemy()
DB_NAME = "data.db"

def create_app():
    app = Flask(__name__)

    # Configure the app secret key
    app.config['SECRET_KEY'] = 'D24A228C7FDE71AB555C4E8EEAC5E'#app_secrets.SECRET_KEY
    
    # Configure the database and initialize it
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    with app.app_context():
        db.create_all()

    # Register the blueprints
    from .pages import pages
    from .auth import auth

    app.register_blueprint(pages, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth/")

    # Create the database
    from .models import Users, Notes

    create_database(app)
        
    # Configure the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    

    return app


def create_database(appName):
    if not path.exists('website/' + DB_NAME):
        with appName.app_context():
            db.create_all()
            print("Database created!")