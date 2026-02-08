# TaskFlow - New Features Documentation

## Overview
This document describes the new Jira-like features added to TaskFlow, including notifications, comments, labels, activity tracking, and enhanced task management.

---

## 🔔 Email Notifications

### Description
Automatic email notifications are sent to users when:
- A task is assigned to them
- A task assigned to them is updated (status, priority, etc.)
- Someone comments on a task assigned to them

### Configuration
1. Copy `.env.example` to `.env` in the backend directory
2. Configure email settings:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=TaskFlow <your-email@gmail.com>
ENABLE_EMAIL_NOTIFICATIONS=True
```

### For Gmail Users
1. Enable 2-Factor Authentication on your Google Account
2. Generate an App Password: https://myaccount.google.com/apppasswords
3. Use the app password in `MAIL_PASSWORD` field

### Notification Templates
- **Task Assignment**: Styled email with task details, priority, due date, and link to view task
- **Task Update**: Email showing what changed (old value → new value)
- **New Comment**: Email with comment content and task context

---

## 📝 Comments & Activity Log

### Comments
- **Add Comments**: Click on any task card to open the task details modal, then use the comments tab
- **View Comments**: All comments are displayed with author name and timestamp
- **Edit/Delete**: Users can edit or delete their own comments
- **Notifications**: Task assignees are notified when new comments are added

### Activity Log
- **Automatic Tracking**: All task changes are automatically logged
- **Tracked Actions**:
  - Task creation
  - Task updates (status, priority, assignee changes)
  - Task assignment
  - Comments added
- **View Activity**: Available in the task details modal under the "Activity" tab
- **Details Shown**: Who made the change, what changed, old → new values, timestamp

### API Endpoints
```
GET    /api/tasks/<task_id>/comments        - Get all comments
POST   /api/tasks/<task_id>/comments        - Add comment
PUT    /api/tasks/comments/<comment_id>     - Update comment
DELETE /api/tasks/comments/<comment_id>     - Delete comment
GET    /api/tasks/<task_id>/activity        - Get activity log
```

---

## 🏷️ Labels/Tags System

### Description
Organize tasks with color-coded labels. Labels are project-specific and can be created by project owners.

### Features
- **Create Labels**: Project owners can create custom labels with names and colors
- **Color-Coded**: Each label has a custom hex color for easy visual identification
- **Add to Tasks**: Assign multiple labels to any task
- **Remove Labels**: Remove labels from tasks without deleting the label itself
- **Filter by Label**: (Future enhancement) Filter tasks by label

### Usage
1. **Create Label**: In project details, go to Labels section → Add Label
2. **Choose Color**: Pick a color using the color picker
3. **Add to Task**: Click on a task → Add labels from the dropdown
4. **Remove from Task**: Click the × button next to the label in task details

### API Endpoints
```
GET    /api/projects/<project_id>/labels              - Get project labels
POST   /api/projects/<project_id>/labels              - Create label
PUT    /api/projects/labels/<label_id>                - Update label
DELETE /api/projects/labels/<label_id>                - Delete label
POST   /api/projects/tasks/<task_id>/labels/<label_id> - Add label to task
DELETE /api/projects/tasks/<task_id>/labels/<label_id> - Remove label from task
```

---

## 👤 Task Assignment & Assignee Management

### Description
Assign tasks to team members with automatic notifications.

### Features
- **Assignee Selection**: Choose from project members when creating/editing tasks
- **Visual Indicator**: Tasks show assignee name and avatar/icon
- **Assignment Notification**: Assignee receives email when task is assigned to them
- **Reassignment**: Change assignee at any time; both old and new assignees are notified
- **Unassigned Tasks**: Tasks can remain unassigned until ready

### Task Card Display
- Shows assignee name with user icon
- Displays due date with calendar icon
- Shows comment count with message icon

---

## 🎯 Enhanced Task Management

### Task Details Modal
Click any task card to open a comprehensive modal with:
- **Task Information**: Full task details with all metadata
- **Quick Edit**: Edit task directly in the modal
- **Assignee Management**: Change who the task is assigned to
- **Labels**: Add/remove labels
- **Comments Tab**: View and add comments
- **Activity Tab**: See complete history of changes

### Task Creation Enhancements
- **Due Date**: Set due dates for tasks
- **Assignee**: Assign to team member immediately
- **Priority Levels**: LOW, MEDIUM, HIGH with visual indicators
- **Rich Descriptions**: Full text descriptions for context

### Task Status Flow
Click the status badge on any task card to cycle through:
- TODO → IN_PROGRESS → DONE → TODO

---

## 🔐 Environment Configuration

### Backend (.env)
```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
FLASK_ENV=development
FLASK_DEBUG=True

# Database Configuration
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/taskflow

# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=TaskFlow <your-email@gmail.com>

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Notification Settings
ENABLE_EMAIL_NOTIFICATIONS=True
```

### Frontend (.env)
```env
VITE_API_URL=http://localhost:5000
```

---

## 📊 Database Schema Updates

### New Tables
1. **comments**: Store task comments
   - id, content, task_id, user_id, created_at, updated_at

2. **labels**: Project-specific labels
   - id, name, color, project_id, created_at

3. **task_labels**: Many-to-many relationship
   - task_id, label_id

4. **activity_logs**: Track all task changes
   - id, task_id, user_id, action, field_changed, old_value, new_value, created_at

### Updated Tables
- **tasks**: Now includes `assigned_to` field (already existed from initial design)

---

## 🚀 Backend Service Architecture

### New Services
1. **notification_service.py**: Handles all notifications and activity logging
   - `send_email()`: Send HTML emails asynchronously
   - `log_activity()`: Record task changes
   - `notify_task_assignment()`: Send assignment emails
   - `notify_task_update()`: Send update emails
   - `notify_comment_added()`: Send comment notifications

### Updated Services
- **task_service.py**: Enhanced with notification triggers

### New Routes
- **comment_routes.py**: CRUD operations for comments
- **label_routes.py**: Label management and task labeling

---

## 🎨 Frontend Components

### New Components
1. **TaskDetailsModal.jsx**: Comprehensive task management modal
   - Edit task inline
   - View/add comments
   - View activity log
   - Manage labels
   - Change assignee

2. **LabelBadge.jsx**: Reusable label display component
   - Color-coded badges
   - Optional remove button
   - Consistent styling

### Updated Components
- **TaskCard.jsx**: 
  - Added labels display
  - Added comment count
  - Added click handler for modal
  - Shows assignee information

### Updated Pages
- **ProjectDetails.jsx**:
  - Labels management section
  - Integrated TaskDetailsModal
  - Enhanced member selection with dropdown
  - Better task creation form

---

## 📈 Future Enhancements

### Planned Features
1. **File Attachments**: Upload files to tasks
2. **Sprint Management**: Organize tasks in sprints
3. **Board View**: Drag-and-drop Kanban board
4. **Time Tracking**: Log time spent on tasks
5. **Custom Fields**: Project-specific custom fields
6. **Webhooks**: Integrate with external services
7. **Advanced Search**: Full-text search across tasks
8. **Reports & Analytics**: Task completion metrics
9. **Due Date Reminders**: Scheduled email reminders
10. **Watchers**: Users can watch tasks for updates

---

## 🔧 Development Notes

### Type Safety
- All new Python files use proper type hints
- SQLAlchemy relationship warnings suppressed with `# type: ignore`
- Frontend uses PropTypes for component validation

### Performance Considerations
- Email sending happens in background threads (non-blocking)
- Activity logs use database indexing on task_id
- Comments use pagination-ready queries

### Security
- All routes protected with JWT authentication
- Project membership verified for all operations
- Only comment authors can edit/delete their comments
- Only project owners can manage labels

---

## 📞 API Summary

### Comments
- `GET /api/tasks/<task_id>/comments`
- `POST /api/tasks/<task_id>/comments`
- `PUT /api/tasks/comments/<comment_id>`
- `DELETE /api/tasks/comments/<comment_id>`

### Labels
- `GET /api/projects/<project_id>/labels`
- `POST /api/projects/<project_id>/labels`
- `PUT /api/projects/labels/<label_id>`
- `DELETE /api/projects/labels/<label_id>`
- `POST /api/projects/tasks/<task_id>/labels/<label_id>`
- `DELETE /api/projects/tasks/<task_id>/labels/<label_id>`

### Activity
- `GET /api/tasks/<task_id>/activity`

### Existing Enhanced Endpoints
- `POST /api/tasks` - Now triggers assignment notifications
- `PUT /api/tasks/<task_id>` - Now logs activity and sends notifications
- `GET /api/auth/users` - Get all users (for assignee dropdown)

---

## ✅ Testing Checklist

- [ ] Create a label with custom color
- [ ] Add label to a task
- [ ] Remove label from a task
- [ ] Assign a task to a user
- [ ] Verify assignment email received
- [ ] Update task status and priority
- [ ] Verify update email received
- [ ] Add a comment to a task
- [ ] Verify comment email received
- [ ] View activity log for task changes
- [ ] Edit a task in the details modal
- [ ] Test with email notifications disabled

---

## 📝 Migration Guide

### From Previous Version
1. Install new dependencies:
   ```bash
   cd backend
   pip install Flask-Mail==0.10.0
   ```

2. Create .env file from .env.example

3. Restart backend server (database tables auto-create)

4. Test new features in the UI

### Database Migration
The app uses `db.create_all()` for automatic table creation. For production, consider using Flask-Migrate:
```bash
flask db init
flask db migrate -m "Add comments, labels, activity logs"
flask db upgrade
```

---

*Last Updated: February 8, 2026*
*Version: 2.0.0*
