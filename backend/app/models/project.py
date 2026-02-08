from datetime import datetime
from typing import Optional, List
from app.extensions import db


class ProjectMember(db.Model):
    """Association model for project members with roles"""
    __tablename__ = "project_members"
    
    user_id: int = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    project_id: int = db.Column(db.Integer, db.ForeignKey("projects.id"), primary_key=True)
    role: str = db.Column(db.Enum("PM", "MEMBER", name="project_role"), default="MEMBER", nullable=False)
    added_at: datetime = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", backref=db.backref("project_memberships", lazy="dynamic"))
    project = db.relationship("Project", backref=db.backref("project_memberships", lazy="dynamic"))
    
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "project_id": self.project_id,
            "role": self.role,
            "added_at": self.added_at.isoformat() if self.added_at else None,
            "user": self.user.to_dict() if self.user else None
        }


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
    
    @property
    def members(self) -> List:
        """Get all project members (both PM and regular members)"""
        from app.models.user import User
        memberships = ProjectMember.query.filter_by(project_id=self.id).all()
        return [User.query.get(m.user_id) for m in memberships]
    
    @property
    def project_managers(self) -> List:
        """Get users with PM role for this project"""
        from app.models.user import User
        memberships = ProjectMember.query.filter_by(project_id=self.id, role="PM").all()
        return [User.query.get(m.user_id) for m in memberships]
    
    def get_user_role(self, user_id: int) -> Optional[str]:
        """Get the role of a user in this project"""
        membership = ProjectMember.query.filter_by(project_id=self.id, user_id=user_id).first()
        return membership.role if membership else None
    
    def is_project_manager(self, user_id: int) -> bool:
        """Check if user is a PM for this project"""
        return self.get_user_role(user_id) == "PM"
    
    def is_member(self, user_id: int) -> bool:
        """Check if user is a member (PM or regular) of this project"""
        return ProjectMember.query.filter_by(project_id=self.id, user_id=user_id).first() is not None

    def to_dict(self, include_tasks=False):
        # Get all memberships with roles
        memberships = ProjectMember.query.filter_by(project_id=self.id).all()
        members_with_roles = []
        for membership in memberships:
            from app.models.user import User
            user = User.query.get(membership.user_id)
            if user:
                user_dict = user.to_dict()
                user_dict['project_role'] = membership.role
                members_with_roles.append(user_dict)
        
        data = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner_id": self.owner_id,
            "owner": self.owner.to_dict() if self.owner else None,
            "members": members_with_roles,
            "project_managers": [pm.to_dict() for pm in self.project_managers],
            "task_count": self.tasks.count(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        if include_tasks:
            data["tasks"] = [t.to_dict() for t in self.tasks.all()]
        return data
