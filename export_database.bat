@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
:: Database Export Script - Health Management System

echo ========================================
echo Exporting Database...
echo ========================================
echo.

:: 请求用户输入数据库密码
set /p MYSQL_PWD=Please enter MySQL root password: 
echo.

:: Create backup directory
if not exist "database_backup" mkdir database_backup

:: Set backup filename with timestamp
set BACKUP_FILE=database_backup\health_db_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%.sql

:: Export database structure and data
echo [1/2] Exporting database structure and data...
mysqldump -u root -p%MYSQL_PWD% --default-character-set=utf8mb4 --routines --triggers health_db > "%BACKUP_FILE%"