import logging
import time
from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS
from sqlalchemy.exc import OperationalError

from . import auth, routes
from .config import Config
from .models import db


def _init_db_with_retry(app: Flask, retries: int = 10, delay_seconds: int = 2) -> None:
    """Initialize DB tables, retrying on transient OperationalError failures."""
    with app.app_context():
        for attempt in range(1, retries + 1):
            try:
                db.create_all()
                return
            except OperationalError as error:
                if attempt == retries:
                    raise
                app.logger.warning(
                    "Database not ready (attempt %s/%s): %s. Retrying in %ss...",
                    attempt,
                    retries,
                    error,
                    delay_seconds,
                )
                time.sleep(delay_seconds)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    CORS(app)

    logging.basicConfig(level=logging.INFO)
    Path(app.config["UPLOAD_DIR"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    _init_db_with_retry(app)

    auth.register_routes(app)
    routes.register_routes(app)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.exception("Unhandled error: %s", error)
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
