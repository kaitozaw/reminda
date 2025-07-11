from app.extensions import celery, csrf, db, login_manager, migrate
from app.routes import register_routes
from config import Config
from flask import Flask
from flask_cors import CORS
import logging

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)
    
    from app.models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    register_routes(app)

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["CELERY_RESULT_BACKEND"],
        timezone="Australia/Brisbane",
        enable_utc=False,
    )
    celery.Task.app = app

    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)

    return app