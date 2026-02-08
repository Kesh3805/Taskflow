from typing import Optional, Tuple, List
from app.extensions import db
from app.models.project import Project, project_members
from app.models.user import User


class ProjectService:
    @staticmethod
    def create_project(name: str, description: Optional[str], owner_id: int) -> Project:
        project = Project(name=name, description=description, owner_id=owner_id)
        # Auto-add owner as a member
        owner = User.query.get(owner_id)
        if owner:
            project.members.append(owner)
        db.session.add(project)
        db.session.commit()
        return project

    @staticmethod
    def get_all_projects(user_id: int, user_role: str) -> List[Project]:
        if user_role == "ADMIN":
            return Project.query.order_by(Project.created_at.desc()).all()  # type: ignore
        # Members see only projects they own or are members of
        return Project.query.filter(
            db.or_(
                Project.owner_id == user_id,
                Project.members.any(User.id == user_id),
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
    def add_member(project: Project, user_id: int) -> Tuple[Optional[Project], Optional[str]]:
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        if user in project.members:
            return None, "User is already a member"
        project.members.append(user)
        db.session.commit()
        return project, None

    @staticmethod
    def remove_member(project: Project, user_id: int) -> Tuple[Optional[Project], Optional[str]]:
        user = User.query.get(user_id)
        if not user:
            return None, "User not found"
        if user not in project.members:
            return None, "User is not a member"
        if project.owner_id == user_id:
            return None, "Cannot remove the project owner"
        project.members.remove(user)
        db.session.commit()
        return project, None

    @staticmethod
    def is_project_member(project: Project, user_id: int) -> bool:
        return any(m.id == user_id for m in project.members) or project.owner_id == user_id  # type: ignore
