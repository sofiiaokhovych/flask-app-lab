from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from .config import config
import os


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import main_bp
    from .users import user_bp
    from .products import products_bp
    from .posts import post_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(post_bp, url_prefix="/post")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("404.html", title="404"), 404

    return app