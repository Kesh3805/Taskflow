from typing import Optional, List, Dict, Any
from datetime import date
from app.extensions import db
from app.models.task import Task


class TaskService:
    @staticmethod
    def create_task(title: str, description: Optional[str], project_id: int,
                    assigned_to: Optional[int] = None, priority: str = "MEDIUM",
                    due_date: Optional[date] = None, creator_id: Optional[int] = None) -> Task:
        task = Task(
            title=title,
            description=description,
            project_id=project_id,
            assigned_to=assigned_to,
            priority=priority,
            due_date=due_date,
        )
        db.session.add(task)
        db.session.commit()
        
        # Send notification if task is assigned and we have creator info
        if assigned_to and creator_id and assigned_to != creator_id:
            from app.services.notification_service import notify_task_assignment
            notify_task_assignment(task.id, assigned_to, creator_id)
        
        # Log activity
        if creator_id:
            from app.services.notification_service import log_activity
            log_activity(task.id, creator_id, "created")
        
        return task

    @staticmethod
    def get_tasks_by_project(project_id: int, status: Optional[str] = None,
                            priority: Optional[str] = None) -> List[Task]:
        query = Task.query.filter_by(project_id=project_id)
        if status:
            query = query.filter_by(status=status)
        if priority:
            query = query.filter_by(priority=priority)
        return query.order_by(Task.created_at.desc()).all()  # type: ignore

    @staticmethod
    def get_task_by_id(task_id: int) -> Optional[Task]:
        return Task.query.get(task_id)

    @staticmethod
    def update_task(task: Task, updater_id: Optional[int] = None, **kwargs) -> Task:
        allowed_fields = ["title", "description", "status", "priority", "assigned_to", "due_date"]
        
        # Track changes for notifications
        old_assigned_to = task.assigned_to
        old_status = task.status
        old_priority = task.priority
        
        for field in allowed_fields:
            if field in kwargs and kwargs[field] is not None:
                setattr(task, field, kwargs[field])
        
        db.session.commit()
        
        # Send notifications and log activities if updater is provided
        if updater_id:
            from app.services.notification_service import notify_task_assignment, notify_task_update, log_activity
            
            # Notify if assignee changed
            if "assigned_to" in kwargs and kwargs["assigned_to"] is not None:
                new_assigned_to = kwargs["assigned_to"]
                if new_assigned_to != old_assigned_to and new_assigned_to != updater_id:
                    notify_task_assignment(task.id, new_assigned_to, updater_id)
            
            # Notify if status changed
            if "status" in kwargs and kwargs["status"] != old_status:
                notify_task_update(task.id, updater_id, "status", old_status, kwargs["status"])
            
            # Notify if priority changed
            if "priority" in kwargs and kwargs["priority"] != old_priority:
                notify_task_update(task.id, updater_id, "priority", old_priority, kwargs["priority"])
        
        return task

    @staticmethod
    def delete_task(task: Task) -> None:
        db.session.delete(task)
        db.session.commit()

    @staticmethod
    def get_task_summary(project_id: int) -> Dict[str, int]:
        tasks = Task.query.filter_by(project_id=project_id).all()
        summary = {"total": len(tasks), "TODO": 0, "IN_PROGRESS": 0, "DONE": 0}
        for t in tasks:
            summary[t.status] = summary.get(t.status, 0) + 1
        return summary
