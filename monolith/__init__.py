from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_dropzone import Dropzone

from config import config, Config
from celery import Celery

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()
dropzone = Dropzone()

celery = Celery(
    __name__,
    broker=Config.CELERY_BROKER_URL,
    include=["monolith.services.background.tasks"],
)
celery.autodiscover_tasks(["monolith.services.background.tasks"], force=True)


def create_app(config_name, updated_variables=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    dropzone.init_app(app)
    if updated_variables:
        app.config.update(updated_variables)

    config[config_name].init_app(app)

    context = app.app_context()
    context.push()

    from monolith.views import blueprints

    for bp in blueprints:
        app.register_blueprint(bp)
        bp.app = app

    login_manager.init_app(app)
    db.init_app(app)
    db.create_all(app=app)
    mail.init_app(app)
    celery.conf.update(app.config)

    return app
