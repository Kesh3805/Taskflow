from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.comment import Comment
from app.models.task import Task
from app.models.project import Project
from app.services.notification_service import notify_comment_added
from typing import Optional

comment_bp = Blueprint("comment", __name__)


@comment_bp.route("/<int:task_id>/comments", methods=["GET"])
@jwt_required()
def get_comments(task_id: int):
    """Get all comments for a task"""
    try:
        current_user_id: int = get_jwt_identity()
        
        # Check if task exists and user has access
        task: Optional[Task] = db.session.get(Task, task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        project: Optional[Project] = db.session.get(Project, task.project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Check if user is project member or owner
        is_owner = project.owner_id == current_user_id
        is_member = any(member.id == current_user_id for member in project.members)  # type: ignore
        
        if not is_owner and not is_member:
            return jsonify({"error": "Access denied"}), 403
        
        comments = Comment.query.filter_by(task_id=task_id).order_by(Comment.created_at.desc()).all()  # type: ignore
        return jsonify([comment.to_dict() for comment in comments]), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/<int:task_id>/comments", methods=["POST"])
@jwt_required()
def create_comment(task_id: int):
    """Create a new comment on a task"""
    try:
        current_user_id: int = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        content = data.get("content")
        if not content or not content.strip():
            return jsonify({"error": "Comment content is required"}), 400
        
        # Check if task exists and user has access
        task: Optional[Task] = db.session.get(Task, task_id)
        if not task:
            return jsonify({"error": "Task not found"}), 404
        
        project: Optional[Project] = db.session.get(Project, task.project_id)
        if not project:
            return jsonify({"error": "Project not found"}), 404
        
        # Check if user is project member or owner
        is_owner = project.owner_id == current_user_id
        is_member = any(member.id == current_user_id for member in project.members)  # type: ignore
        
        if not is_owner and not is_member:
            return jsonify({"error": "Access denied"}), 403
        
        # Create comment
        comment = Comment(
            content=content.strip(),
            task_id=task_id,
            user_id=current_user_id
        )
        
        db.session.add(comment)
        db.session.commit()
        
        # Send notification
        notify_comment_added(task_id, current_user_id, content.strip())
        
        return jsonify(comment.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/comments/<int:comment_id>", methods=["PUT"])
@jwt_required()
def update_comment(comment_id: int):
    """Update a comment"""
    try:
        current_user_id: int = get_jwt_identity()
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No data provided"}), 400
        
        comment: Optional[Comment] = db.session.get(Comment, comment_id)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Only comment author can update
        if comment.user_id != current_user_id:
            return jsonify({"error": "You can only edit your own comments"}), 403
        
        content = data.get("content")
        if content is not None:
            if not content.strip():
                return jsonify({"error": "Comment content cannot be empty"}), 400
            comment.content = content.strip()
        
        db.session.commit()
        return jsonify(comment.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@comment_bp.route("/comments/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id: int):
    """Delete a comment"""
    try:
        current_user_id: int = get_jwt_identity()
        
        comment: Optional[Comment] = db.session.get(Comment, comment_id)
        if not comment:
            return jsonify({"error": "Comment not found"}), 404
        
        # Only comment author can delete
        if comment.user_id != current_user_id:
            return jsonify({"error": "You can only delete your own comments"}), 403
        
        db.session.delete(comment)
        db.session.commit()
        
        return jsonify({"message": "Comment deleted successfully"}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
