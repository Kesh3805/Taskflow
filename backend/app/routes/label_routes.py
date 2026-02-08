from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.label import Label
from app.models.task import Task
from app.models.project import Project
from typing import Optional

label_bp = Blueprint("label", __name__)


@label_bp.route("/projects/<int:project_id>/labels", methods=["GET"])
@jwt_required()
def get_project_labels(project_id: int):
    """Get all labels for a project"""
    try:
        current_user_id: int = get_jwt_identity()
        
        project: Optional[Project] = db.session.get(Project, project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Check if user has access to project
        is_owner = project.owner_id == current_user_id
        is_member = any(member.id == current_user_id for member in project.members)  # type: ignore
        
        if not is_owner and not is_member:
            return jsonify({"error": "Access denied"}), 403
        
        labels = Label.query.filter_by(project_id=project_id).order_by(Label.name).all()
        return jsonify([label.to_dict() for label in labels]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@label_bp.route("/projects/<int:project_id>/labels", methods=["POST"])
@jwt_required()
def create_label(project_id: int):
    """Create a new label for a project"""
    try:
        current_user_id: int = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        project: Optional[Project] = db.session.get(Project, project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Only project owner can create labels
        if project.owner_id != current_user_id:
            return jsonify({"error": "Only project owner can create labels"}), 403
        
        name = data.get("name")
        color = data.get("color", "#6b7280")  # Default gray color
        
        if not name or not name.strip():
            return jsonify({"error": "Label name is required"}), 400
        
        # Check if label with same name exists in project
        existing_label = Label.query.filter_by(project_id=project_id, name=name.strip()).first()
        if existing_label:
            return jsonify({"error": "Label with this name already exists"}), 400
        
        label = Label(
            name=name.strip(),
            color=color,
            project_id=project_id
        )
        
        db.session.add(label)
        db.session.commit()
        
        return jsonify(label.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@label_bp.route("/labels/<int:label_id>", methods=["PUT"])
@jwt_required()
def update_label(label_id: int):
    """Update a label"""
    try:
        current_user_id: int = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        label: Optional[Label] = db.session.get(Label, label_id)
        if not label:
            return jsonify({"error": "Label not found"}), 404
        
        project: Optional[Project] = db.session.get(Project, label.project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Only project owner can update labels
        if project.owner_id != current_user_id:
            return jsonify({"error": "Only project owner can update labels"}), 403
        
        name = data.get("name")
        color = data.get("color")
        
        if name is not None:
            if not name.strip():
                return jsonify({"error": "Label name cannot be empty"}), 400
            
            # Check if another label with same name exists
            existing_label = Label.query.filter(  # type: ignore
                Label.project_id == label.project_id,
                Label.name == name.strip(),
                Label.id != label_id
            ).first()
            if existing_label:
                return jsonify({"error": "Label with this name already exists"}), 400
            
            label.name = name.strip()
        
        if color is not None:
            label.color = color
        
        db.session.commit()
        return jsonify(label.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@label_bp.route("/labels/<int:label_id>", methods=["DELETE"])
@jwt_required()
def delete_label(label_id: int):
    """Delete a label"""
    try:
        current_user_id: int = get_jwt_identity()
        
        label: Optional[Label] = db.session.get(Label, label_id)
        if not label:
            return jsonify({"error": "Label not found"}), 404
        
        project: Optional[Project] = db.session.get(Project, label.project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Only project owner can delete labels
        if project.owner_id != current_user_id:
            return jsonify({"error": "Only project owner can delete labels"}), 403
        
        db.session.delete(label)
        db.session.commit()
        
        return jsonify({"message": "Label deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@label_bp.route("/tasks/<int:task_id>/labels/<int:label_id>", methods=["POST"])
@jwt_required()
def add_label_to_task(task_id: int, label_id: int):
    """Add a label to a task"""
    try:
        current_user_id: int = get_jwt_identity()
        
        task: Optional[Task] = db.session.get(Task, task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        label: Optional[Label] = db.session.get(Label, label_id)
        if not label:
            return jsonify({"error": "Label not found"}), 404
        
        # Check if label belongs to task's project
        if label.project_id != task.project_id:
            return jsonify({"error": "Label does not belong to this project"}), 400
        
        project: Optional[Project] = db.session.get(Project, task.project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Check if user has access
        is_owner = project.owner_id == current_user_id
        is_member = any(member.id == current_user_id for member in project.members)  # type: ignore
        
        if not is_owner and not is_member:
            return jsonify({"error": "Access denied"}), 403
        
        # Add label to task if not already added
        if label not in task.labels:  # type: ignore
            task.labels.append(label)  # type: ignore
            db.session.commit()
        
        return jsonify(task.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@label_bp.route("/tasks/<int:task_id>/labels/<int:label_id>", methods=["DELETE"])
@jwt_required()
def remove_label_from_task(task_id: int, label_id: int):
    """Remove a label from a task"""
    try:
        current_user_id: int = get_jwt_identity()
        
        task: Optional[Task] = db.session.get(Task, task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        label: Optional[Label] = db.session.get(Label, label_id)
        if not label:
            return jsonify({"error": "Label not found"}), 404
        
        project: Optional[Project] = db.session.get(Project, task.project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Check if user has access
        is_owner = project.owner_id == current_user_id
        is_member = any(member.id == current_user_id for member in project.members)  # type: ignore
        
        if not is_owner and not is_member:
            return jsonify({"error": "Access denied"}), 403
        
        # Remove label from task
        if label in task.labels:  # type: ignore
            task.labels.remove(label)  # type: ignore
            db.session.commit()
        
        return jsonify(task.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
