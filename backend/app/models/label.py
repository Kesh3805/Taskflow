from datetime import datetime
from typing import Optional
from app.extensions import db

# Association table for many-to-many relationship between tasks and labels
task_labels = db.Table(
    "task_labels",
    db.Column("task_id", db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"), primary_key=True),
    db.Column("label_id", db.Integer, db.ForeignKey("labels.id", ondelete="CASCADE"), primary_key=True),
)


class Label(db.Model):
    __tablename__ = "labels"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name: str = db.Column(db.String(50), nullable=False)
    color: str = db.Column(db.String(7), nullable=False)  # Hex color code (e.g., #FF5733)
    project_id: int = db.Column(db.Integer, db.ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    project = db.relationship("Project", backref=db.backref("labels", lazy="dynamic", cascade="all, delete-orphan"))
    tasks = db.relationship("Task", secondary=task_labels, backref="labels", lazy="dynamic")

    def __init__(self, name: str, color: str, project_id: int, **kwargs):
        super().__init__(**kwargs)
        self.name = name
        self.color = color
        self.project_id = project_id

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "color": self.color,
            "project_id": self.project_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
