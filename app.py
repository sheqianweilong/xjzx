from flask import Flask
from flask_wtf.csrf import CSRFProtect

from views_news import news_blueprint
from views_user import user_blueprint
from views_admin import admin_blueprint
from configs import Config


def create_app(config):
    app = Flask(__name__, static_folder=Config.STATIC_FOLDER, template_folder=Config.TEMPLATES_FOLDER)
    app.config.from_object(config)
    CSRFProtect(app)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)
    app.register_blueprint(admin_blueprint)
    return app
