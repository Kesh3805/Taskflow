<div align="center">

# 🚀 TaskFlow

### Modern Task Management & Team Collaboration Platform

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18.3.1-61dafb.svg)](https://reactjs.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg)](https://www.mysql.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

*A powerful, full-stack task management system inspired by Jira, built with Flask & React*

[Features](#-features) • [Demo](#-demo) • [Installation](#-installation) • [Usage](#-usage) • [Tech Stack](#-tech-stack)

</div>

---

## ✨ Features

### 🎯 Core Task Management
- **Projects & Tasks** - Organize work with projects containing multiple tasks
- **Status Tracking** - Todo, In Progress, In Review, Done
- **Priority Levels** - Low, Medium, High, Critical
- **Due Dates** - Calendar integration with deadline tracking
- **Task Assignment** - Assign tasks to team members

### 🔔 Notifications & Collaboration
- **Email Notifications** - Automatic alerts for task assignments and updates
- **Comments System** - Rich discussion threads on every task
- **Activity Logs** - Complete audit trail of all task changes
- **Real-time Updates** - Instant UI updates across the team

### 🏷️ Organization & Search
- **Smart Labels** - Color-coded tags for easy categorization
- **Advanced Filtering** - Filter by status, priority, assignee, labels
- **Full-text Search** - Find tasks quickly across projects

### 🔐 Security & Authentication
- **JWT Authentication** - Secure token-based auth system
- **Password Hashing** - Bcrypt encryption for user credentials
- **Protected Routes** - API and frontend route protection
- **Session Management** - Automatic token refresh
- **Role-Based Access Control** - Granular permissions for admins and members

### 👥 Role-Based Permissions

**ADMIN Role:**
- ✅ Create new projects
- ✅ View and manage all projects
- ✅ Full access to all features
- ✅ Override project owner permissions
- ✅ System-wide management capabilities

**Project OWNER:**
- ✅ Manage project settings (edit, delete)
- ✅ Add/remove project members
- ✅ Create and delete labels
- ✅ Full task management
- ✅ View activity logs and analytics

**Project MEMBER:**
- ✅ View project details
- ✅ Create, edit, and delete tasks
- ✅ Add comments on tasks
- ✅ Use existing labels (cannot create new ones)
- ✅ View team members and activity
- ❌ Cannot modify project settings
- ❌ Cannot add/remove members
- ❌ Cannot create/delete labels

---

## 🎨 Screenshots

> **Coming Soon** - Add screenshots of your application here!

---

## 🛠️ Tech Stack

### Backend
- **Framework:** Flask 3.1.0
- **Database:** MySQL 8.0+ with SQLAlchemy ORM
- **Authentication:** Flask-JWT-Extended
- **Email:** Flask-Mail (SMTP)
- **Migrations:** Flask-Migrate (Alembic)
- **Security:** Werkzeug, cryptography

### Frontend
- **Framework:** React 18.3.1
- **Build Tool:** Vite 6.4.1
- **Routing:** React Router v6
- **HTTP Client:** Axios
- **Icons:** React Icons
- **Styling:** Custom CSS with modern design

### DevOps
- **Version Control:** Git & GitHub
- **Database:** MySQL
- **Development:** Hot reload for both frontend & backend

---

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **MySQL 8.0+** - [Download](https://dev.mysql.com/downloads/)
- **Git** - [Download](https://git-scm.com/downloads)

---

## 🚀 Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Kesh3805/Taskflow.git
cd TaskFlow
```

### 2️⃣ Database Setup

Create the MySQL database:

```sql
CREATE DATABASE taskflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or use the provided script:

```bash
mysql -u root -p < setup_database.sql
```

### 3️⃣ Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies (no venv needed)
python -m pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your database credentials and email settings

# Initialize database tables
python init_db.py

# (Optional) Seed with sample data
python seed_db.py
```

### 4️⃣ Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Configure environment variables
cp .env.example .env
# Edit .env if needed (default backend URL is http://localhost:5000)
```

### 5️⃣ Run the Application

**Backend Server:**
```bash
cd backend
python run.py
```
✅ Backend running at: `http://localhost:5000`

**Frontend Server:**
```bash
cd frontend
npm run dev
```
✅ Frontend running at: `http://localhost:3000` or `http://localhost:3001`

---

## 🎮 Usage

### Default Test Credentials

After running `seed_db.py`, you can login with:

- **Admin User:**
  - Email: `admin@taskflow.com`
  - Password: `admin123`

- **Regular User:**
  - Email: `user@taskflow.com`
  - Password: `user123`

### Quick Start Guide

1. **Register/Login** - Create an account or use test credentials
2. **Create a Project** - Click "New Project" on the dashboard
3. **Add Team Members** - Invite users to your project
4. **Create Tasks** - Add tasks with titles, descriptions, priorities
5. **Assign & Track** - Assign tasks to members and track progress
6. **Collaborate** - Comment on tasks and view activity logs
7. **Organize** - Use labels and filters to manage workload

---

## 📡 API Endpoints

### 🔐 Authentication
| Method | Endpoint              | Description        | Auth Required |
|--------|-----------------------|--------------------|---------------|
| POST   | `/api/auth/register`  | Register new user  | ❌            |
| POST   | `/api/auth/login`     | Login user         | ❌            |
| GET    | `/api/auth/profile`   | Get current user   | ✅            |

### 📁 Projects
| Method | Endpoint                                  | Description          | Auth Required |
|--------|-------------------------------------------|----------------------|---------------|
| POST   | `/api/projects`                           | Create project       | ✅            |
| GET    | `/api/projects`                           | List user projects   | ✅            |
| GET    | `/api/projects/<id>`                      | Get project details  | ✅            |
| PUT    | `/api/projects/<id>`                      | Update project       | ✅            |
| DELETE | `/api/projects/<id>`                      | Delete project       | ✅            |
| POST   | `/api/projects/<id>/members`              | Add member           | ✅            |
| DELETE | `/api/projects/<id>/members/<user_id>`    | Remove member        | ✅            |

### ✅ Tasks
| Method | Endpoint                        | Description           | Auth Required |
|--------|---------------------------------|-----------------------|---------------|
| POST   | `/api/tasks`                    | Create task           | ✅            |
| GET    | `/api/tasks/project/<project_id>` | List project tasks  | ✅            |
| GET    | `/api/tasks/<id>`               | Get task details      | ✅            |
| PUT    | `/api/tasks/<id>`               | Update task           | ✅            |
| DELETE | `/api/tasks/<id>`               | Delete task           | ✅            |

### 💬 Comments
| Method | Endpoint                        | Description           | Auth Required |
|--------|---------------------------------|-----------------------|---------------|
| POST   | `/api/tasks/<id>/comments`      | Add comment           | ✅            |
| GET    | `/api/tasks/<id>/comments`      | Get task comments     | ✅            |

### 🏷️ Labels
| Method | Endpoint                        | Description           | Auth Required |
|--------|---------------------------------|-----------------------|---------------|
| POST   | `/api/labels`                   | Create label          | ✅            |
| GET    | `/api/labels`                   | List all labels       | ✅            |
| POST   | `/api/tasks/<id>/labels`        | Add label to task     | ✅            |
| DELETE | `/api/tasks/<task_id>/labels/<label_id>` | Remove label | ✅            |

---

## 📂 Project Structure

```
TaskFlow/
├── 📁 backend/
│   ├── 📁 app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── config.py            # Configuration settings
│   │   ├── extensions.py        # SQLAlchemy, JWT, Mail, Migrate
│   │   ├── 📁 models/           # Database models
│   │   │   ├── user.py          # User model
│   │   │   ├── project.py       # Project model
│   │   │   ├── task.py          # Task model
│   │   │   ├── comment.py       # Comment model
│   │   │   ├── label.py         # Label model
│   │   │   └── activity_log.py  # Activity tracking
│   │   ├── 📁 routes/           # API endpoints
│   │   │   ├── auth_routes.py   # Authentication routes
│   │   │   ├── project_routes.py
│   │   │   ├── task_routes.py
│   │   │   ├── comment_routes.py
│   │   │   └── label_routes.py
│   │   ├── 📁 services/         # Business logic
│   │   │   ├── notification_service.py
│   │   │   ├── task_service.py
│   │   │   └── project_service.py
│   │   └── 📁 utils/            # Helper functions
│   │       └── auth_middleware.py
│   ├── run.py                   # Application entry point
│   ├── init_db.py              # Database initialization
│   ├── seed_db.py              # Sample data seeder
│   ├── requirements.txt         # Python dependencies
│   ├── .env.example            # Environment template
│   └── .env                    # Environment variables (create this)
│
├── 📁 frontend/
│   ├── 📁 src/
│   │   ├── 📁 api/
│   │   │   └── axios.js         # HTTP client with JWT
│   │   ├── 📁 components/       # React components
│   │   │   ├── Navbar.jsx
│   │   │   ├── TaskCard.jsx
│   │   │   ├── ProjectCard.jsx
│   │   │   ├── TaskDetailsModal.jsx
│   │   │   └── LabelBadge.jsx
│   │   ├── 📁 context/          # React Context
│   │   │   └── AuthContext.jsx  # Authentication state
│   │   ├── 📁 pages/            # Application pages
│   │   │   ├── Login.jsx
│   │   │   ├── Register.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── ProjectDetails.jsx
│   │   │   └── Tasks.jsx
│   │   ├── App.jsx              # Root component
│   │   ├── main.jsx            # Entry point
│   │   └── index.css           # Global styles
│   ├── index.html
│   ├── vite.config.js          # Vite configuration
│   ├── package.json            # Node dependencies
│   ├── .env.example            # Environment template
│   └── .env                    # Environment variables (create this)
│
├── 📄 README.md                 # This file
├── 📄 .gitignore               # Git ignore rules
├── 📄 setup_database.sql        # Database creation script
├── 📄 SETUP.md                 # Detailed setup guide
├── 📄 FEATURES.md              # Feature documentation
└── 📄 TEST_CREDENTIALS.md      # Test account information
```

---

## 🔧 Configuration

### Backend Environment Variables (`.env`)

```env
# Flask Configuration
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-here
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
MAIL_DEFAULT_SENDER=TaskFlow <noreply@taskflow.com>

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Notification Settings
ENABLE_EMAIL_NOTIFICATIONS=True
```

### Frontend Environment Variables (`.env`)

```env
VITE_API_BASE_URL=http://localhost:5000
```

---

## 🧪 Testing

### Manual Testing

Test accounts are available after seeding:

```bash
cd backend
python seed_db.py
```

See [TEST_CREDENTIALS.md](TEST_CREDENTIALS.md) for login details.

### Testing Email Notifications

For development, use [Ethereal Email](https://ethereal.email) (fake SMTP):

```env
MAIL_SERVER=smtp.ethereal.email
MAIL_PORT=587
MAIL_USERNAME=your-ethereal-username
MAIL_PASSWORD=your-ethereal-password
```

Check captured emails at https://ethereal.email

---

## 🚢 Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` and `JWT_SECRET_KEY` to strong random values
- [ ] Set `FLASK_ENV=production` and `FLASK_DEBUG=False`
- [ ] Use a production database with proper credentials
- [ ] Configure real SMTP service (Gmail, SendGrid, AWS SES)
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure CORS for your production domain
- [ ] Use a production WSGI server (Gunicorn, uWSGI)
- [ ] Set up environment variables securely
- [ ] Configure database backups
- [ ] Set up monitoring and logging

### Recommended Stack

- **Frontend:** Vercel, Netlify, or AWS Amplify
- **Backend:** AWS EC2, DigitalOcean, Heroku, or Railway
- **Database:** AWS RDS (MySQL), PlanetScale, or managed MySQL
- **Email:** SendGrid, AWS SES, or Mailgun

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add some amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### Development Guidelines

- Follow PEP 8 for Python code
- Use ESLint/Prettier for JavaScript code
- Write descriptive commit messages
- Add comments for complex logic
- Update documentation for new features
- Test your changes thoroughly

---

## 🐛 Known Issues

- Email notifications require SMTP configuration
- File attachments not yet implemented (coming soon!)
- Mobile responsiveness needs improvement on some screens

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Kesh3805**

- GitHub: [@Kesh3805](https://github.com/Kesh3805)
- Repository: [TaskFlow](https://github.com/Kesh3805/Taskflow)

---

## 🙏 Acknowledgments

- Flask framework and its amazing extensions
- React and Vite for the modern frontend tooling
- The open-source community for inspiration and tools
- All contributors who help improve this project

---

## 📞 Support

If you encounter any issues or have questions:

- 🐛 [Report a Bug](https://github.com/Kesh3805/Taskflow/issues)
- 💡 [Request a Feature](https://github.com/Kesh3805/Taskflow/issues)
- 📧 Email: (Add your email here)

---

<div align="center">

### ⭐ Star this repository if you find it helpful!
</div>

