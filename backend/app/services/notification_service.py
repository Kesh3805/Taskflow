from flask import current_app
from flask_mail import Message
from app.extensions import mail, db
from app.models.user import User
from app.models.task import Task
from app.models.activity_log import ActivityLog
from typing import Optional
import threading


def send_async_email(app, msg):
    """Send email asynchronously"""
    with app.app_context():
        try:
            mail.send(msg)
        except Exception as e:
            print(f"Error sending email: {str(e)}")


def send_email(subject: str, recipients: list, html_body: str):
    """Send email notification"""
    if not current_app.config.get("ENABLE_EMAIL_NOTIFICATIONS"):
        print(f"Email notifications disabled. Would have sent: {subject} to {recipients}")
        return

    if not current_app.config.get("MAIL_USERNAME"):
        print("Email not configured. Skipping notification.")
        return

    try:
        msg = Message(
            subject=subject,
            recipients=recipients,
            html=html_body,
            sender=current_app.config.get("MAIL_DEFAULT_SENDER")
        )
        
        # Send email in background thread
        app = current_app._get_current_object()  # type: ignore
        thread = threading.Thread(target=send_async_email, args=(app, msg))
        thread.start()
    except Exception as e:
        print(f"Error creating email: {str(e)}")


def log_activity(task_id: int, user_id: int, action: str, 
                field_changed: Optional[str] = None,
                old_value: Optional[str] = None, 
                new_value: Optional[str] = None):
    """Log activity for a task"""
    try:
        activity = ActivityLog(
            task_id=task_id,
            user_id=user_id,
            action=action,
            field_changed=field_changed,
            old_value=old_value,
            new_value=new_value
        )
        db.session.add(activity)
        db.session.commit()
    except Exception as e:
        print(f"Error logging activity: {str(e)}")
        db.session.rollback()


def notify_task_assignment(task_id: int, assignee_id: int, assigner_id: int):
    """Send notification when a task is assigned"""
    try:
        task = db.session.get(Task, task_id)
        assignee = db.session.get(User, assignee_id)
        assigner = db.session.get(User, assigner_id)
        
        if not task or not assignee or not assigner:
            return

        # Log activity
        log_activity(
            task_id=task_id,
            user_id=assigner_id,
            action="assigned",
            field_changed="assignee",
            new_value=assignee.name
        )

        # Send email notification
        frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:3000")
        task_url = f"{frontend_url}/projects/{task.project_id}"
        
        subject = f"Task Assigned: {task.title}"
        html_body = f"""
        <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #2563eb;">Task Assigned to You</h2>
                    <p>Hi {assignee.name},</p>
                    <p><strong>{assigner.name}</strong> has assigned a task to you:</p>
                    
                    <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <h3 style="margin-top: 0; color: #1f2937;">{task.title}</h3>
                        <p style="margin-bottom: 10px;"><strong>Priority:</strong> <span style="color: {'#dc2626' if task.priority == 'HIGH' else '#f59e0b' if task.priority == 'MEDIUM' else '#10b981'};">{task.priority}</span></p>
                        <p style="margin-bottom: 10px;"><strong>Status:</strong> {task.status}</p>
                        {f'<p style="margin-bottom: 10px;"><strong>Due Date:</strong> {task.due_date.strftime("%B %d, %Y")}</p>' if task.due_date else ''}
                        {f'<p style="margin-bottom: 0;"><strong>Description:</strong><br/>{task.description}</p>' if task.description else ''}
                    </div>
                    
                    <a href="{task_url}" style="display: inline-block; background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">View Task</a>
                    
                    <p style="margin-top: 30px; color: #6b7280; font-size: 14px;">
                        This is an automated notification from TaskFlow. Please do not reply to this email.
                    </p>
                </div>
            </body>
        </html>
        """
        
        send_email(subject=subject, recipients=[assignee.email], html_body=html_body)
        
    except Exception as e:
        print(f"Error sending task assignment notification: {str(e)}")


def notify_task_update(task_id: int, updater_id: int, field_changed: str, old_value: str, new_value: str):
    """Send notification when a task is updated"""
    try:
        task = db.session.get(Task, task_id)
        updater = db.session.get(User, updater_id)
        
        if not task or not updater:
            return

        # Log activity
        log_activity(
            task_id=task_id,
            user_id=updater_id,
            action="updated",
            field_changed=field_changed,
            old_value=old_value,
            new_value=new_value
        )

        # Send email to assignee if task is assigned and updater is not the assignee
        if task.assigned_to and task.assigned_to != updater_id:
            assignee = db.session.get(User, task.assigned_to)
            if not assignee:
                return

            frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:3000")
            task_url = f"{frontend_url}/projects/{task.project_id}"
            
            subject = f"Task Updated: {task.title}"
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2563eb;">Task Updated</h2>
                        <p>Hi {assignee.name},</p>
                        <p><strong>{updater.name}</strong> updated a task assigned to you:</p>
                        
                        <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #1f2937;">{task.title}</h3>
                            <p style="margin-bottom: 10px;"><strong>Changed:</strong> {field_changed}</p>
                            <p style="margin-bottom: 10px;"><strong>From:</strong> {old_value}</p>
                            <p style="margin-bottom: 0;"><strong>To:</strong> {new_value}</p>
                        </div>
                        
                        <a href="{task_url}" style="display: inline-block; background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">View Task</a>
                        
                        <p style="margin-top: 30px; color: #6b7280; font-size: 14px;">
                            This is an automated notification from TaskFlow. Please do not reply to this email.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            send_email(subject=subject, recipients=[assignee.email], html_body=html_body)
            
    except Exception as e:
        print(f"Error sending task update notification: {str(e)}")


def notify_comment_added(task_id: int, commenter_id: int, comment_content: str):
    """Send notification when a comment is added to a task"""
    try:
        task = db.session.get(Task, task_id)
        commenter = db.session.get(User, commenter_id)
        
        if not task or not commenter:
            return

        # Notify assignee if someone else commented
        if task.assigned_to and task.assigned_to != commenter_id:
            assignee = db.session.get(User, task.assigned_to)
            if not assignee:
                return

            frontend_url = current_app.config.get("FRONTEND_URL", "http://localhost:3000")
            task_url = f"{frontend_url}/projects/{task.project_id}"
            
            subject = f"New Comment on: {task.title}"
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                    <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                        <h2 style="color: #2563eb;">New Comment</h2>
                        <p>Hi {assignee.name},</p>
                        <p><strong>{commenter.name}</strong> commented on a task assigned to you:</p>
                        
                        <div style="background-color: #f3f4f6; padding: 15px; border-radius: 5px; margin: 20px 0;">
                            <h3 style="margin-top: 0; color: #1f2937;">{task.title}</h3>
                            <p style="margin-bottom: 0;"><strong>Comment:</strong><br/>{comment_content}</p>
                        </div>
                        
                        <a href="{task_url}" style="display: inline-block; background-color: #2563eb; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; margin-top: 10px;">View Task</a>
                        
                        <p style="margin-top: 30px; color: #6b7280; font-size: 14px;">
                            This is an automated notification from TaskFlow. Please do not reply to this email.
                        </p>
                    </div>
                </body>
            </html>
            """
            
            send_email(subject=subject, recipients=[assignee.email], html_body=html_body)
            
    except Exception as e:
        print(f"Error sending comment notification: {str(e)}")
