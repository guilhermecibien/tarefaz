import os

from flask import Flask

from app.datas import rotulo_prazo
from app.models.database import init_app as init_database


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "chave-de-desenvolvimento"),
        DATABASE=os.path.join(app.instance_path, "tarefaz.sqlite"),
    )

    if test_config:
        app.config.update(test_config)

    os.makedirs(app.instance_path, exist_ok=True)
    init_database(app)
    app.jinja_env.filters["rotulo"] = rotulo_prazo

    from app.controllers.auth_controller import auth_bp
    from app.controllers.task_controller import task_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(task_bp)

    return app
