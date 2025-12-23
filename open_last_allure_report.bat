@echo off
echo Opening last Allure report...

if not exist "reports\allure-results" (
    echo ERROR: No Allure results found!
    echo Run tests first: run_tests_with_allure.bat
    exit /b 1
)

REM Open the report
allure serve reports\allure-results