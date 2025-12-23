#!/bin/bash

echo "Opening last Allure report..."

if [ ! -d "reports/allure-results" ]; then
    echo "ERROR: No Allure results found!"
    echo "Run tests first: ./run_tests_with_allure.sh"
    exit 1
fi

# Open the report (automatically generates HTML from results)
allure serve reports/allure-results