from flask import Flask

from extensions import api
from api.products import blp


def create_app():
    app = Flask(__name__)

    app.config["API_TITLE"] = "Product API"
    app.config["API_VERSION"] = "1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"

    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = (
        "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    )

    api.init_app(app)
    api.register_blueprint(blp)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5000)
