-- TaskFlow Database Setup Script
-- Run this with: mysql -u root -p < setup_database.sql

CREATE DATABASE IF NOT EXISTS taskflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE taskflow;

-- Show confirmation
SELECT 'Database taskflow created successfully!' AS Status;
SHOW DATABASES LIKE 'taskflow';
