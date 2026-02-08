from typing import Optional, Tuple, List
from app.extensions import db
from app.models.project import Project, ProjectMember
from app.models.user import User


class ProjectService:
    @staticmethod
    def create_project(name: str, description: Optional[str], owner_id: int) -> Project:
        project = Project(name=name, description=description, owner_id=owner_id)
        db.session.add(project)
        db.session.flush()  # Get the project ID
        
        # Auto-add owner as PM (Project Manager)
        owner_membership = ProjectMember(user_id=owner_id, project_id=project.id, role="PM")
        db.session.add(owner_membership)
        db.session.commit()
        return project

    @staticmethod
    def get_all_projects(user_id: int, user_role: str) -> List[Project]:
        if user_role == "ADMIN":
            return Project.query.order_by(Project.created_at.desc()).all()  # type: ignore
        # Members see only projects they own or are members of
        member_project_ids = [m.project_id for m in ProjectMember.query.filter_by(user_id=user_id).all()]
        return Project.query.filter(
            db.or_(
                Project.owner_id == user_id,
                Project.id.in_(member_project_ids)
            )
        ).order_by(Project.created_at.desc()).all()  # type: ignore

    @staticmethod
    def get_project_by_id(project_id: int) -> Optional[Project]:
        return Project.query.get(project_id)

    @staticmethod
    def update_project(project: Project, name: Optional[str] = None, description: Optional[str] = None) -> Project:
        if name:
            project.name = name
        if description is not None:
            project.description = description
        db.session.commit()
        return project

    @staticmethod
    def delete_project(project: Project) -> None:
        db.session.delete(project)
        db.session.commit()

    @staticmethod
    def add_member(project: Project, user_id: int, role: str = "MEMBER") -> Tuple[Optional[Project], Optional[str]]:
        """Add a member to the project with specified role (PM or MEMBER)"""
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        
        existing = ProjectMember.query.filter_by(project_id=project.id, user_id=user_id).first()
        if existing:
            return None, "User is already a member"
        
        # Validate role
        if role not in ["PM", "MEMBER"]:
            role = "MEMBER"
        
        membership = ProjectMember(user_id=user_id, project_id=project.id, role=role)
        db.session.add(membership)
        db.session.commit()
        return project, None

    @staticmethod
    def remove_member(project: Project, user_id: int) -> Tuple[Optional[Project], Optional[str]]:
        membership = ProjectMember.query.filter_by(project_id=project.id, user_id=user_id).first()
        if not membership:
            return None, "User is not a member"
        if project.owner_id == user_id:
            return None, "Cannot remove the project owner"
        db.session.delete(membership)
        db.session.commit()
        return project, None
    
    @staticmethod
    def update_member_role(project: Project, user_id: int, new_role: str) -> Tuple[Optional[Project], Optional[str]]:
        """Update a member's role (PM or MEMBER)"""
        membership = ProjectMember.query.filter_by(project_id=project.id, user_id=user_id).first()
        if not membership:
            return None, "User is not a member"
        
        if new_role not in ["PM", "MEMBER"]:
            return None, "Invalid role"
        
        membership.role = new_role
        db.session.commit()
        return project, None

    @staticmethod
    def is_project_member(project: Project, user_id: int) -> bool:
        """Check if user is any kind of member (PM or regular)"""
        return project.is_member(user_id)
    
    @staticmethod
    def is_project_manager(project: Project, user_id: int) -> bool:
        """Check if user is a PM for this project"""
        return project.is_project_manager(user_id)
    
    @staticmethod
    def has_pm_access(project: Project, user_id: int, user_role: str) -> bool:
        """Check if user has PM-level access (ADMIN system-wide or PM for this project)"""
        return user_role == "ADMIN" or project.is_project_manager(user_id)
