from datetime import datetime
from typing import Optional
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = "users"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(120), nullable=False)
    email: str = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash: str = db.Column(db.String(256), nullable=False)
    role: str = db.Column(db.Enum("ADMIN", "MEMBER", name="user_role"), default="MEMBER", nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name: str, email: str, role: str = "MEMBER", **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.email = email
        self.role = role

    # Relationships
    owned_projects = db.relationship("Project", backref="owner", lazy="dynamic", foreign_keys="Project.owner_id")
    assigned_tasks = db.relationship("Task", backref="assignee", lazy="dynamic", foreign_keys="Task.assigned_to")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
