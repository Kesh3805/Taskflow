from flask import Flask
from flask_cors import CORS
from app.extensions import db, jwt, migrate, mail
from app.config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.project_routes import project_bp
    from app.routes.task_routes import task_bp
    from app.routes.comment_routes import comment_bp
    from app.routes.label_routes import label_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(project_bp, url_prefix="/api/projects")
    app.register_blueprint(task_bp, url_prefix="/api/tasks")
    app.register_blueprint(comment_bp, url_prefix="/api/tasks")
    app.register_blueprint(label_bp, url_prefix="/api/projects")

    # Create tables
    with app.app_context():
        from app.models import user, project, task, comment, label, activity_log  # noqa: F401
        db.create_all()

    return app
