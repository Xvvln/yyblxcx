@echo off
chcp 936 >nul
:: 检查管理员权限
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo 请求管理员权限...
    :: 使用PowerShell以管理员身份重新运行此脚本
    powershell -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo 正在启动MySQL服务...
net start mysql

if %errorLevel% equ 0 (
    echo MySQL服务启动成功！
) else (
    echo MySQL服务启动失败，请检查服务名称是否正确。
    echo 如果服务名称不是"mysql"，请修改脚本中的服务名称。
    pause
)

