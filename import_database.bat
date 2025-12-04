@echo off
chcp 936 >nul
:: 数据库导入脚本 - 营养不良筛查与健康管理系统

echo ========================================
echo 正在导入数据库...
echo ========================================
echo.

:: 检查是否有备份文件
if not exist "database_backup" (
    echo 错误：找不到database_backup目录
    echo 请确保备份文件在database_backup目录中
    pause
    exit /b 1
)

:: 查找最新的备份文件
for /f "delims=" %%i in ('dir "database_backup\health_db_backup_*.sql" /b /o:-d 2^>nul') do (
    set BACKUP_FILE=database_backup\%%i
    goto :found_backup
)

echo 错误：找不到数据库备份文件
echo 请确保有health_db_backup_*.sql文件在database_backup目录中
pause
exit /b 1

:found_backup
echo 找到备份文件: %BACKUP_FILE%

:: 确认导入操作
echo.
echo 警告：此操作将覆盖现有的health_db数据库！
echo 确定要继续吗？(输入 y 继续，其他键取消)
set /p choice=
if /i not "!choice!"=="y" (
    echo 操作已取消
    pause
    exit /b 0
)

:: 删除现有数据库（如果存在）
echo [1/4] 删除现有数据库...
mysql -u root -p1234 -e "DROP DATABASE IF EXISTS health_db;"

if %errorlevel% neq 0 (
    echo     删除数据库失败
    pause
    exit /b 1
)

:: 创建新数据库
echo [2/4] 创建新数据库...
mysql -u root -p1234 -e "CREATE DATABASE health_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %errorlevel% neq 0 (
    echo     创建数据库失败
    pause
    exit /b 1
)

:: 导入数据库结构和数据
echo [3/4] 导入数据库结构和数据...
mysql -u root -p1234 --default-character-set=utf8mb4 health_db < "%BACKUP_FILE%"

if %errorlevel% neq 0 (
    echo     导入数据失败
    pause
    exit /b 1
)

:: 验证导入结果
echo [4/4] 验证导入结果...
mysql -u root -p1234 -e "USE health_db; SHOW TABLES;" > nul 2>&1

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo 数据库导入成功！
    echo ========================================
    echo.
    echo 已导入的数据库: health_db
    echo 备份文件: %BACKUP_FILE%
    echo.
    echo 下一步操作建议:
    echo   1. 检查后端配置文件中的数据库连接信息
    echo   2. 启动后端服务进行测试
    echo   3. 检查前端是否能正常连接API
    echo.
) else (
    echo     数据库验证失败
    pause
    exit /b 1
)

pause








