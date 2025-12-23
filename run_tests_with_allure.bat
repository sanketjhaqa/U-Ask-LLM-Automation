@echo off
echo ==========================================
echo Running Tests with Allure Report
echo ==========================================

REM Run tests
pytest -v %*

REM Check if Allure is installed
where allure >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Allure is not installed!
    echo Install with: scoop install allure
    echo.
    echo Opening HTML report instead...
    start reports\report.html
    exit /b 1
)

echo.
echo ==========================================
echo Generating Allure Report...
echo ==========================================

REM Generate and open Allure report
allure serve reports\allure-results

echo.
echo Report opened in browser!