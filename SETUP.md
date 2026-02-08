# TaskFlow Setup Instructions

## Step 1: Create MySQL Database

Run the following command to create the database:

```powershell
mysql -u root -p < setup_database.sql
```

Or manually in MySQL:
```sql
CREATE DATABASE IF NOT EXISTS taskflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Step 2: Update Database Configuration (if needed)

Edit `backend/app/config.py` and update the database URL:
```python
SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/taskflow"
```

Or set environment variable:
```powershell
$env:DATABASE_URL="mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/taskflow"
```

## Step 3: Initialize Database Tables

```powershell
cd backend
C:/Users/user/Desktop/TaskFlow/.venv/Scripts/python.exe init_db.py
```

## Step 4: Run Backend Server

```powershell
cd backend
C:/Users/user/Desktop/TaskFlow/.venv/Scripts/python.exe run.py
```

The API will be available at http://localhost:5000

## Step 5: Install Frontend Dependencies

```powershell
cd frontend
npm install
```

## Step 6: Run Frontend

```powershell
cd frontend
npm run dev
```

The app will be available at http://localhost:3000

## Quick Start (After Initial Setup)

### Terminal 1 - Backend:
```powershell
cd C:\Users\user\Desktop\TaskFlow\backend
C:/Users/user/Desktop/TaskFlow/.venv/Scripts/python.exe run.py
```

### Terminal 2 - Frontend:
```powershell
cd C:\Users\user\Desktop\TaskFlow\frontend
npm run dev
```
