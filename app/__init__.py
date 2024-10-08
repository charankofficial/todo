from flask import Flask
from flask_session import Session

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'CHAN'
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)

    from .auth import auth
    from .views import views

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
