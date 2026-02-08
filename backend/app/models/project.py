from datetime import datetime
from typing import Optional
from app.extensions import db

# Association table for project members
project_members = db.Table(
    "project_members",
    db.Column("user_id", db.Integer, db.ForeignKey("users.id"), primary_key=True),
    db.Column("project_id", db.Integer, db.ForeignKey("projects.id"), primary_key=True),
)


class Project(db.Model):
    __tablename__ = "projects"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(200), nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)
    owner_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name: str, description: Optional[str], owner_id: int, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.description = description
        self.owner_id = owner_id

    # Relationships
    tasks = db.relationship("Task", backref="project", lazy="dynamic", cascade="all, delete-orphan")
    members = db.relationship("User", secondary=project_members, backref=db.backref("projects", lazy="dynamic"))

    def to_dict(self, include_tasks=False):
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "owner": self.owner.to_dict() if self.owner else None,
            "members": [m.to_dict() for m in self.members],
            "task_count": self.tasks.count(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_tasks:
            data["tasks"] = [t.to_dict() for t in self.tasks.all()]
        return data
