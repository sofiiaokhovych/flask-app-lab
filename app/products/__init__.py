from flask import Blueprint

products_bp = Blueprint("products",
                        __name__,
                        url_prefix="/products",
                        template_folder="templates/products",
                        static_folder="static",
                        static_url_path="/static"
                        )

@products_bp.record_once
def set_upload_limit(state):
    state.app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024

from app.products import views