from datetime import datetime, date
from typing import Optional
from app.extensions import db


class Task(db.Model):
    __tablename__ = "tasks"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title: str = db.Column(db.String(200), nullable=False)
    description: Optional[str] = db.Column(db.Text, nullable=True)
    status: str = db.Column(
        db.Enum("TODO", "IN_PROGRESS", "DONE", name="task_status"),
        default="TODO",
        nullable=False,
    )
    priority: str = db.Column(
        db.Enum("LOW", "MEDIUM", "HIGH", name="task_priority"),
        default="MEDIUM",
        nullable=False,
    )
    project_id: int = db.Column(db.Integer, db.ForeignKey("projects.id"), nullable=False)
    assigned_to: Optional[int] = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    due_date: Optional[date] = db.Column(db.Date, nullable=True)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, title: str, description: Optional[str], project_id: int,
                 assigned_to: Optional[int] = None, priority: str = "MEDIUM",
                 due_date: Optional[date] = None, **kwargs):
        super().__init__(**kwargs)
        self.title = title
        self.description = description
        self.project_id = project_id
        self.assigned_to = assigned_to
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "project_id": self.project_id,
            "assigned_to": self.assigned_to,
            "assignee": self.assignee.to_dict() if self.assignee else None,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "labels": [label.to_dict() for label in self.labels] if hasattr(self, 'labels') else [],  # type: ignore
            "comment_count": self.comments.count() if hasattr(self, 'comments') else 0,
        }
