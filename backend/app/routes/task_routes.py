from datetime import datetime
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.auth_middleware import get_current_user, validate_required_fields
from app.services.task_service import TaskService
from app.services.project_service import ProjectService
from app.models.activity_log import ActivityLog
from typing import Optional

task_bp = Blueprint("tasks", __name__)


@task_bp.route("", methods=["POST"])
@jwt_required()
def create_task():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    valid, error = validate_required_fields(data, ["title", "project_id"])
    if not valid:
        return jsonify({"error": error}), 400

    project = ProjectService.get_project_by_id(data["project_id"])
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if user.role != "ADMIN" and not ProjectService.is_project_member(project, user.id):
        return jsonify({"error": "Access denied"}), 403

    due_date = None
    if data.get("due_date"):
        try:
            due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    task = TaskService.create_task(
        title=data["title"],
        description=data.get("description", ""),
        project_id=data["project_id"],
        assigned_to=data.get("assigned_to"),
        priority=data.get("priority", "MEDIUM"),
        due_date=due_date,
        creator_id=user.id,
    )
    return jsonify({"message": "Task created", "task": task.to_dict()}), 201


@task_bp.route("/project/<int:project_id>", methods=["GET"])
@jwt_required()
def get_tasks(project_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    project = ProjectService.get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if user.role != "ADMIN" and not ProjectService.is_project_member(project, user.id):
        return jsonify({"error": "Access denied"}), 403

    status = request.args.get("status")
    priority = request.args.get("priority")
    tasks = TaskService.get_tasks_by_project(project_id, status=status, priority=priority)
    summary = TaskService.get_task_summary(project_id)

    return jsonify({"tasks": [t.to_dict() for t in tasks], "summary": summary}), 200


@task_bp.route("/<int:task_id>", methods=["PUT"])
@jwt_required()
def update_task(task_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    task = TaskService.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    project = ProjectService.get_project_by_id(task.project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    if user.role != "ADMIN" and not ProjectService.is_project_member(project, user.id):
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json()
    due_date = task.due_date
    if "due_date" in data:
        if data["due_date"]:
            try:
                due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
            except ValueError:
                return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400
        else:
            due_date = None

    task = TaskService.update_task(
        task,
        updater_id=user.id,
        title=data.get("title"),
        description=data.get("description"),
        status=data.get("status"),
        priority=data.get("priority"),
        assigned_to=data.get("assigned_to"),
        due_date=due_date,
    )
    return jsonify({"message": "Task updated", "task": task.to_dict()}), 200


@task_bp.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    task = TaskService.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    project = ProjectService.get_project_by_id(task.project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    if user.role != "ADMIN" and not ProjectService.is_project_member(project, user.id):
        return jsonify({"error": "Access denied"}), 403

    TaskService.delete_task(task)
    return jsonify({"message": "Task deleted"}), 200


@task_bp.route("/<int:task_id>/activity", methods=["GET"])
@jwt_required()
def get_task_activity(task_id: int):
    """Get activity logs for a task"""
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    task = TaskService.get_task_by_id(task_id)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    
    project = ProjectService.get_project_by_id(task.project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    
    if user.role != "ADMIN" and not ProjectService.is_project_member(project, user.id):
        return jsonify({"error": "Access denied"}), 403
    
    activities = ActivityLog.query.filter_by(task_id=task_id).order_by(ActivityLog.created_at.desc()).all()  # type: ignore
    return jsonify([activity.to_dict() for activity in activities]), 200
