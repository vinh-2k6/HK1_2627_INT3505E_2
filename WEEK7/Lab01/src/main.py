from flask import Flask, jsonify
from sqlalchemy import text
from werkzeug.exceptions import HTTPException

from src.extensions import db, migrate, api
from src.config import Config
from src.models import Product, Order, OrderItem
from src.api.products import blp as products_blp
from src.api.orders import blp as orders_blp


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)

    # Register blueprints with flask-smorest
    api.register_blueprint(products_blp)
    api.register_blueprint(orders_blp)

    # 4. Separate Health Checks (/healthz and /ready)
    # /healthz: Liveness probe - lightweight, no DB query
    @app.get("/healthz")
    def healthz():
        return jsonify({"status": "ok"}), 200

    # /ready: Readiness probe - verifies DB connectivity
    @app.get("/ready")
    def ready():
        checks = {}
        try:
            db.session.execute(text("SELECT 1"))
            checks["db"] = "ok"
            return jsonify({
                "status": "ready",
                "database": "connected",
                "checks": checks
            }), 200
        except Exception as error:
            app.logger.error(f"Readiness check failed: {error}")
            checks["db"] = "err"
            return jsonify({
                "status": "not ready",
                "database": "disconnected",
                "checks": checks
            }), 503

    return app
