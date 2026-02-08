from datetime import datetime
from typing import Optional
from app.extensions import db


class Comment(db.Model):
    __tablename__ = "comments"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content: str = db.Column(db.Text, nullable=False)
    task_id: int = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at: Optional[datetime] = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    task = db.relationship("Task", backref=db.backref("comments", lazy="dynamic", cascade="all, delete-orphan"))
    author = db.relationship("User", backref="comments", foreign_keys=[user_id])

    def __init__(self, content: str, task_id: int, user_id: int, **kwargs):
        super().__init__(**kwargs)
        self.content = content
        self.task_id = task_id
        self.user_id = user_id

    def to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "author": self.author.to_dict() if self.author else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
