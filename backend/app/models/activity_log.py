from datetime import datetime
from typing import Optional
from app.extensions import db


class ActivityLog(db.Model):
    """Activity log for tracking changes to tasks"""
    __tablename__ = "activity_logs"

    id: int = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task_id: int = db.Column(db.Integer, db.ForeignKey("tasks.id", ondelete="CASCADE"), nullable=False)
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    action: str = db.Column(db.String(50), nullable=False)  # e.g., 'created', 'updated', 'assigned', 'commented'
    field_changed: Optional[str] = db.Column(db.String(50), nullable=True)  # e.g., 'status', 'priority', 'assignee'
    old_value: Optional[str] = db.Column(db.String(200), nullable=True)
    new_value: Optional[str] = db.Column(db.String(200), nullable=True)
    created_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    task = db.relationship("Task", backref=db.backref("activity_logs", lazy="dynamic", cascade="all, delete-orphan"))
    user = db.relationship("User", backref="activity_logs", foreign_keys=[user_id])

    def __init__(self, task_id: int, user_id: int, action: str,
                 field_changed: Optional[str] = None, old_value: Optional[str] = None,
                 new_value: Optional[str] = None, **kwargs):
        super().__init__(**kwargs)
        self.task_id = task_id
        self.user_id = user_id
        self.action = action
        self.field_changed = field_changed
        self.old_value = old_value
        self.new_value = new_value

    def to_dict(self):
        return {
            "id": self.id,
            "task_id": self.task_id,
            "user_id": self.user_id,
            "user": self.user.to_dict() if self.user else None,
            "action": self.action,
            "field_changed": self.field_changed,
            "old_value": self.old_value,
            "new_value": self.new_value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
