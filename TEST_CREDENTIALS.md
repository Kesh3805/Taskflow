# 🔐 TaskFlow Test Credentials

## Test Accounts

| Role   | Email                    | Password   | Description                |
|--------|--------------------------|------------|----------------------------|
| ADMIN  | admin@taskflow.com       | admin123   | Full access to all projects |
| MEMBER | alice@taskflow.com       | alice123   | Project owner & member      |
| MEMBER | bob@taskflow.com         | bob123     | Team member                 |
| MEMBER | charlie@taskflow.com     | charlie123 | Team member                 |

## Sample Data Overview

### Projects (3)
1. **Website Redesign** - Owner: Admin
   - Members: Admin, Alice, Bob
   - Tasks: 5 (1 Done, 1 In Progress, 3 Todo)

2. **Mobile App Development** - Owner: Alice
   - Members: Alice, Bob, Charlie
   - Tasks: 6 (2 Done, 2 In Progress, 2 Todo)

3. **Marketing Campaign Q1** - Owner: Bob
   - Members: Bob, Charlie, Admin
   - Tasks: 5 (1 Done, 2 In Progress, 2 Todo)

### Tasks (16 total)
- ✅ Done: 5 tasks
- 🔄 In Progress: 5 tasks
- 📝 To Do: 6 tasks

## Quick Start

1. **Start Backend:**
   ```powershell
   cd backend
   C:/Users/user/Desktop/TaskFlow/.venv/Scripts/python.exe run.py
   ```

2. **Start Frontend (new terminal):**
   ```powershell
   cd frontend
   npm run dev
   ```

3. **Access Application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:5000

4. **Login** with any test account above and explore!
