import connexion


def create_app():
    app = connexion.FlaskApp(__name__, specification_dir="openapi/")

    app.add_api("products.yaml", validate_responses=True)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(port=8080)
