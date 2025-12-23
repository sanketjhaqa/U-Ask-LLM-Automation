#!/bin/bash

echo "=========================================="
echo "Running Tests with Allure Report"
echo "=========================================="

# Run tests
pytest -v "$@"

# Check if tests ran successfully
if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "Tests completed! Generating Allure report..."
    echo "=========================================="

    # Generate and open Allure report
    allure serve reports/allure-results
else
    echo ""
    echo "=========================================="
    echo "Tests failed! Opening report anyway..."
    echo "=========================================="

    # Still show report even if tests failed
    allure serve reports/allure-results
fi