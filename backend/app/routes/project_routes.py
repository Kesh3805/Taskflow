from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.utils.auth_middleware import get_current_user, admin_required, validate_required_fields
from app.services.project_service import ProjectService

project_bp = Blueprint("projects", __name__)


@project_bp.route("", methods=["POST"])
@jwt_required()
def create_project():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    valid, error = validate_required_fields(data, ["name"])
    if not valid:
        return jsonify({"error": error}), 400

    project = ProjectService.create_project(
        name=data["name"],
        description=data.get("description", ""),
        owner_id=user.id,
    )
    return jsonify({"message": "Project created", "project": project.to_dict()}), 201


@project_bp.route("", methods=["GET"])
@jwt_required()
def get_projects():
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    projects = ProjectService.get_all_projects(user.id, user.role)
    return jsonify({"projects": [p.to_dict() for p in projects]}), 200


@project_bp.route("/<int:project_id>", methods=["GET"])
@jwt_required()
def get_project(project_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    project = ProjectService.get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if user.role != "ADMIN" and not ProjectService.is_project_member(project, user.id):
        return jsonify({"error": "Access denied"}), 403

    return jsonify({"project": project.to_dict(include_tasks=True)}), 200


@project_bp.route("/<int:project_id>", methods=["PUT"])
@jwt_required()
def update_project(project_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    project = ProjectService.get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if user.role != "ADMIN" and project.owner_id != user.id:
        return jsonify({"error": "Only the owner or admin can update this project"}), 403

    data = request.get_json()
    project = ProjectService.update_project(
        project,
        name=data.get("name"),
        description=data.get("description"),
    )
    return jsonify({"message": "Project updated", "project": project.to_dict()}), 200


@project_bp.route("/<int:project_id>", methods=["DELETE"])
@jwt_required()
def delete_project(project_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    project = ProjectService.get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if user.role != "ADMIN" and project.owner_id != user.id:
        return jsonify({"error": "Only the owner or admin can delete this project"}), 403

    ProjectService.delete_project(project)
    return jsonify({"message": "Project deleted"}), 200


@project_bp.route("/<int:project_id>/members", methods=["POST"])
@jwt_required()
def add_member(project_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "User not found"}), 404
    project = ProjectService.get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if user.role != "ADMIN" and project.owner_id != user.id:
        return jsonify({"error": "Only the owner or admin can add members"}), 403

    data = request.get_json()
    valid, error = validate_required_fields(data, ["user_id"])
    if not valid:
        return jsonify({"error": error}), 400

    project, error = ProjectService.add_member(project, data["user_id"])
    if error or not project:
        return jsonify({"error": error or "Failed to add member"}), 400

    return jsonify({"message": "Member added", "project": project.to_dict()}), 200


@project_bp.route("/<int:project_id>/members/<int:user_id>", methods=["DELETE"])
@jwt_required()
def remove_member(project_id, user_id):
    current_user = get_current_user()
    if not current_user:
        return jsonify({"error": "User not found"}), 404
    project = ProjectService.get_project_by_id(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404

    if current_user.role != "ADMIN" and project.owner_id != current_user.id:
        return jsonify({"error": "Only the owner or admin can remove members"}), 403

    project, error = ProjectService.remove_member(project, user_id)
    if error or not project:
        return jsonify({"error": error or "Failed to remove member"}), 400

    return jsonify({"message": "Member removed", "project": project.to_dict()}), 200
