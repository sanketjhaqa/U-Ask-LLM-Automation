# 🤖 U-ASK Test Automation Framework

Comprehensive test automation framework for GovGPT application with support for UI, Accessibility, Security, and AI evaluation testing using Playwright and Python.

[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Playwright](https://img.shields.io/badge/playwright-1.57.0-green.svg)](https://playwright.dev/)
[![Pytest](https://img.shields.io/badge/pytest-8.4.2-red.svg)](https://pytest.org/)

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Tests](#running-tests)
- [Test Categories](#test-categories)
- [Reporting](#reporting)
- [Project Structure](#project-structure)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## 🎯 Overview

This framework provides automated testing for the GovGPT government services chatbot application. It includes:

- **43 Test Scenarios** across 4 categories
- **Bilingual Support** - English and Arabic
- **AI Quality Testing** - RAGAS metrics for LLM evaluation
- **Accessibility Testing** - WCAG 2.1 Level AA compliance
- **Security Testing** - XSS, SQL injection, prompt injection
- **Comprehensive Reporting** - HTML reports + Allure dashboard

---

## ✨ Features

### 🎭 Test Coverage
- ✅ **UI Functional Tests (18)** - Chat interface, message sending, loading states
- ✅ **Accessibility Tests (7)** - WCAG compliance, keyboard navigation, screen reader support
- ✅ **Security Tests (10)** - XSS, SQL injection, prompt injection, data leakage
- ✅ **AI/RAGAS Tests (8)** - Faithfulness, relevancy, context recall, topic adherence

### 🌍 Multi-Language Support
- ✅ English language tests (~30 tests)
- ✅ Arabic language tests with RTL layout (~7 tests)
- ✅ Bilingual tests with language switching (~6 tests)

### 📊 Advanced Features
- ✅ **Page Object Model** - Clean, maintainable architecture
- ✅ **Parallel Execution** - Run tests faster with pytest-xdist
- ✅ **Dual Reporting** - pytest-html + Allure interactive reports
- ✅ **Screenshot on Failure** - Automatic capture for debugging
- ✅ **Video Recording** - Optional test execution recording
- ✅ **Mobile Testing** - Responsive design validation (iPhone 12 Pro)
- ✅ **CI/CD Ready** - JUnit XML output

---

## 🚀 Quick Start

### Prerequisites
- **Python 3.12+** ([Download](https://www.python.org/downloads/))
- **Git** ([Download](https://git-scm.com/downloads/))

### Installation (3 Steps)

#### Windows (PowerShell):
```powershell
# 1. Clone and enter directory
git clone <repository-url>
cd perplexity

# 2. Install dependencies
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements_minimal.txt
playwright install chromium

# 3. Run tests
pytest -v
```

#### Linux/Mac:
```bash
# 1. Clone and enter directory
git clone <repository-url>
cd perplexity

# 2. Install dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements_minimal.txt
playwright install chromium

# 3. Run tests
pytest -v
```

### First Test Run
```bash
# Run all tests
pytest -v

# Run specific category
pytest -m ui -v

# View HTML report
# Windows: start reports/report.html
# Mac: open reports/report.html
# Linux: xdg-open reports/report.html
```

---

## 📦 Installation

### Option 1: Automated Setup (Recommended)

```bash
# Ensure you're in the project directory
cd perplexity

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Windows CMD:
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements_minimal.txt

# Install Playwright browsers
playwright install chromium

# Download NLTK data (required for AI tests)
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Option 2: Full Installation (All Features)

For document processing and complete feature set:

```bash
# Install comprehensive dependencies
pip install -r requirements_verified.txt

# Install Playwright browsers
playwright install chromium

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

### Requirements Files Comparison

| File | Packages | Size | Best For |
|------|----------|------|----------|
| **requirements_minimal.txt** | ~25 | ~500 MB | Standard testing (recommended) |
| **requirements_verified.txt** | ~150 | ~2 GB | Full features + document processing |

### Installing Allure CLI (Optional - For Reports)

**Windows (using Scoop):**
```powershell
# Install Scoop first if not installed
iwr -useb get.scoop.sh | iex

# Install Allure
scoop install allure
```

**Mac (using Homebrew):**
```bash
brew install allure
```

**Linux (Ubuntu/Debian):**
```bash
# Install Java (required for Allure)
sudo apt-get update
sudo apt-get install default-jre

# Download and install Allure
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

---

## ⚙️ Configuration

### config.yaml

Located at: `config/config.yaml`

```yaml
# Application URL
base_url: "https://govgpt.sandbox.dge.gov.ae/"

# Test credentials
username: "qatest1@dge.gov.ae"
password: "DGEUser100!"

# General settings
default_language: "en"
timeout_ms: 60000

# API Keys (can also use .env file)
openApiKey: "sk-proj-..."
PERPLEXITY_API_KEY: "pplx-..."
RAGA_APP_TOKEN: ""

# Video Recording Configuration
enable_video_recording: false  # Set to true to enable
video_dir: "videos/"           # Directory to save videos
```

### .env File (Optional)

Create `.env` file in project root for sensitive data:

```env
PERPLEXITY_API_KEY=your-api-key-here
openApiKey=your-openai-key-here
```

**Note:** API keys in `.env` override those in `config.yaml`

---

## ▶️ Running Tests

### Basic Commands

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/ui/test_chat_ui.py -v

# Run specific test function
pytest tests/ui/test_chat_ui.py::test_user_can_send_message -v

# Show print statements (debugging)
pytest -v -s

# Stop on first failure
pytest -v -x

# Run last failed tests only
pytest --lf -v
```

### Run by Category

```bash
# UI functional tests (18 tests)
pytest -m ui -v

# Accessibility tests (7 tests)
pytest -m accessibility -v

# Security tests (10 tests)
pytest -m security -v

# AI/RAGAS evaluation tests (8 tests)
pytest -m ai -v
```

### Run by Language

```bash
# English language tests (~30 tests)
pytest -m english -v

# Arabic language tests (~7 tests)
pytest -m arabic -v

# Bilingual tests (~6 tests)
pytest -m bilingual -v
```

### Advanced Combinations

```bash
# UI tests in English only
pytest -m "ui and english" -v

# Security tests in Arabic
pytest -m "security and arabic" -v

# All AI tests except slow ones
pytest -m "ai and not slow" -v

# All tests except slow tests
pytest -m "not slow" -v
```

### Parallel Execution

```bash
# Run with 4 parallel workers (MUCH FASTER)
pytest -v -n 4

# Run with auto-detected number of CPUs
pytest -v -n auto
```

### Helper Scripts

```bash
# Run tests with automatic Allure report generation

# Windows (PowerShell):
.\run_tests_with_allure.ps1

# Windows (CMD):
run_tests_with_allure.bat

# Linux/Mac:
./run_tests_with_allure.sh

# With specific markers:
.\run_tests_with_allure.ps1 -m "ui and english"
./run_tests_with_allure.sh -m security
```

---

## 🎯 Test Categories

### Test Distribution

| Category | Count | Description | Marker |
|----------|-------|-------------|--------|
| **UI Functional** | 18 | Chat widget, messaging, scrolling, history | `@pytest.mark.ui` |
| **Accessibility** | 7 | WCAG compliance, keyboard nav, ARIA | `@pytest.mark.accessibility` |
| **Security** | 10 | XSS, SQL injection, prompt attacks | `@pytest.mark.security` |
| **AI/RAGAS** | 8 | LLM quality metrics evaluation | `@pytest.mark.ai` |
| **TOTAL** | **43** | | |

### Test Details

#### UI Tests (18)
- `test_chat_widget_loads_desktop` - Desktop view loading
- `test_chat_widget_loads_mobile` - Mobile view loading  
- `test_user_can_send_message` - Message sending functionality
- `test_ai_response_rendered` - AI response display
- `test_input_cleared_after_send` - Input field clearing
- `test_scroll_behavior` - Auto-scroll to new messages
- `test_multiple_messages_sequence` - Multi-turn conversations
- `test_send_button_enabled_with_input` - Button state management
- `test_chat_maintains_history` - History persistence
- Plus 9 multilingual UI tests (RTL/LTR, language switching)

#### Accessibility Tests (7)
- `test_chat_input_has_label` - Input accessibility labels
- `test_keyboard_navigation` - Keyboard-only navigation
- `test_aria_roles_present` - ARIA role validation
- `test_focus_order_left_nav_to_input` - Logical focus order
- `test_buttons_have_accessible_names` - Button labels
- `test_chat_messages_region_has_live_attributes` - Live region announcements
- `test_chat_page_has_no_critical_violations` - axe-core automated scan (90+ rules)

#### Security Tests (10)
- XSS attack prevention (script tags, event handlers, SVG)
- SQL injection blocking
- Prompt injection rejection
- Sensitive data protection (API keys, passwords)
- Path traversal prevention
- Comprehensive security sweep (all 20 attack vectors)

#### AI/RAGAS Tests (8)
- Faithfulness (factual accuracy)
- Response Relevancy (query-answer alignment)
- Context Recall (reference document usage)
- Topic Adherence (conversation coherence)
- Comprehensive quality reporting

---

## 📊 Reporting

### 1. HTML Report (pytest-html)

**Automatic generation** - created after every test run

```bash
# Run tests (report auto-generated)
pytest -v

# View report
# Windows:
start reports/report.html
# Mac:
open reports/report.html
# Linux:
xdg-open reports/report.html
```

**Features:**
- ✅ Single HTML file (easy to share)
- ✅ Pass/Fail summary with percentages
- ✅ Test execution time
- ✅ Screenshots on failure
- ✅ No additional tools required

---

### 2. Allure Report (Interactive Dashboard)

**Generate Allure report:**

```bash
# Run tests (Allure results auto-generated)
pytest -v

# View interactive report (recommended)
allure serve reports/allure-results

# Or generate static HTML
allure generate reports/allure-results -o reports/allure-report --clean
# Then open: reports/allure-report/index.html
```

**Features:**
- ✅ Interactive dashboard with graphs
- ✅ Test categorization and trends
- ✅ Detailed test history
- ✅ Screenshots and attachments
- ✅ Execution timeline
- ✅ Flaky test detection

---

### 3. axe-core Accessibility Report

**Automatic generation** for accessibility tests:

```bash
# Run accessibility tests
pytest -m accessibility -v

# View detailed axe report
# File: reports/axe_chat_page.json
```

This JSON report contains:
- Violations (grouped by severity)
- Help text and fix recommendations
- Affected elements with selectors
- WCAG criteria references

---

## 📁 Project Structure

```
perplexity/
│
├── 📁 config/
│   └── config.yaml                 # Main configuration file
│
├── 📁 data/
│   ├── test_data.json             # Test data (EN/AR test cases)
│   ├── test_data_factory.py      # Test data utilities
│   └── documents/                 # Reference documents for RAGAS
│
├── 📁 logs/
│   └── run_YYYYMMDD_HHMMSS.log   # Test execution logs
│
├── 📁 nltk_data/
│   ├── taggers/                   # NLTK POS tagger data
│   └── tokenizers/                # NLTK tokenizer data (punkt)
│
├── 📁 pages/                       # Page Object Model
│   ├── __init__.py
│   ├── base_page.py               # Base page class
│   ├── chat_page.py               # Chat page object
│   └── login_page.py              # Login page object
│
├── 📁 reports/
│   ├── report.html                # pytest-html report
│   ├── axe_chat_page.json        # axe-core accessibility report
│   ├── allure-results/           # Allure test results
│   └── screenshots/              # Failure screenshots
│
├── 📁 tests/
│   ├── 📁 accessibility/
│   │   ├── test_accessibility.py       # Manual accessibility tests (6)
│   │   └── test_accessibility_axe.py   # Automated axe-core scan (1)
│   │
│   ├── 📁 ai/
│   │   ├── test_ai_responses_en.py     # English AI tests (6)
│   │   ├── test_ai_responses_ar.py     # Arabic AI tests (7)
│   │   ├── test_ragas_metrics.py       # RAGAS evaluation (8)
│   │   └── test_ai_rubric.py           # AI rubric validation
│   │
│   ├── 📁 security/
│   │   └── test_injection.py           # Security tests (10)
│   │
│   └── 📁 ui/
│       ├── test_chat_ui.py             # Chat UI tests (9)
│       └── test_multilingual_ui.py     # Multilingual tests (9)
│
├── 📁 utils/
│   ├── helpers.py                 # Utility functions
│   └── logger.py                  # Logging configuration
│
├── 📁 videos/                      # Test execution videos (optional)
│
├── 📄 conftest.py                  # Pytest fixtures and configuration
├── 📄 pytest.ini                   # Pytest settings and markers
│
├── 📄 requirements_minimal.txt     # Minimal dependencies (~25 packages)
├── 📄 requirements_verified.txt    # Full dependencies (~150 packages)
│
├── 📄 run_tests_with_allure.sh    # Test runner script (Linux/Mac)
├── 📄 run_tests_with_allure.ps1   # Test runner script (Windows PS)
├── 📄 run_tests_with_allure.bat   # Test runner script (Windows CMD)
│
├── 📄 open_last_allure_report.sh  # Open report script (Linux/Mac)
├── 📄 open_last_allure_report.bat # Open report script (Windows)
│
├── 📄 README.md                    # This file
├── 📄 SETUP_GUIDE.md              # Detailed setup instructions
└── 📄 TEST_SCENARIOS_SUMMARY.md   # Test scenarios reference
```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Import Errors / Module Not Found
```bash
# Solution: Ensure virtual environment is activated
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Then reinstall dependencies
pip install -r requirements_minimal.txt
```

#### 2. Playwright Browser Not Found
```bash
# Solution: Install Playwright browsers
playwright install chromium

# If still failing, try:
python -m playwright install chromium
```

#### 3. Allure Command Not Found
```bash
# Windows (using Scoop):
scoop install allure

# Mac (using Homebrew):
brew install allure

# Linux:
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

#### 4. Virtual Environment Activation Fails (Windows)
```powershell
# Error: "execution of scripts is disabled on this system"
# Solution: Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
.\venv\Scripts\Activate.ps1
```

#### 5. NLTK Data Not Found
```bash
# Solution: Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# Or manually:
python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('averaged_perceptron_tagger')
>>> exit()
```

#### 6. Tests Timeout / Connection Errors
```yaml
# Edit config/config.yaml and increase timeout:
timeout_ms: 120000  # Increase from 60000 to 120000

# Check internet connection
# Verify base_url is accessible
```

#### 7. API Key Errors
```bash
# For AI/RAGAS tests, ensure API keys are configured:

# Option 1: Edit config/config.yaml
PERPLEXITY_API_KEY: "your-key-here"
openApiKey: "your-key-here"

# Option 2: Create .env file (recommended)
echo "PERPLEXITY_API_KEY=your-key-here" > .env
echo "openApiKey=your-key-here" >> .env
```

#### 8. Video Recording Issues
```yaml
# If videos not recording, check config/config.yaml:
enable_video_recording: true  # Must be true
video_dir: "videos/"

# Ensure videos directory exists:
mkdir videos
```

---

## 🤝 Contributing

### Adding New Tests

1. **Choose the correct category folder:**
   - `tests/ui/` for UI functional tests
   - `tests/accessibility/` for accessibility tests
   - `tests/security/` for security tests
   - `tests/ai/` for AI/RAGAS tests

2. **Add pytest markers:**
```python
import pytest
import allure

@allure.feature('Feature Name')
@allure.story('User Story')
@pytest.mark.ui
@pytest.mark.english
def test_new_feature(chat_page):
    """Test description"""
    # Test implementation
    pass
```

3. **Follow Page Object Model:**
```python
# Use page objects from pages/ folder
from pages.chat_page import ChatPage

def test_example(chat_page: ChatPage):
    chat_page.send_message("test")
    response = chat_page.get_last_ai_response()
    assert len(response) > 0
```

4. **Add test data to data/test_data.json:**
```json
{
  "en": {
    "category_name": [
      {
        "id": "TEST_001",
        "prompt": "Test query",
        "expected": "Expected result"
      }
    ]
  }
}
```

5. **Run your new tests:**
```bash
pytest tests/your_test_file.py -v -s
```

---

## 📚 Additional Resources

### Documentation
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Detailed setup instructions
- [TEST_SCENARIOS_SUMMARY.md](TEST_SCENARIOS_SUMMARY.md) - Complete test catalog

### External Resources
- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Python](https://playwright.dev/python/)
- [Allure Reports](https://docs.qameta.io/allure/)
- [RAGAS Documentation](https://docs.ragas.io/)
- [axe-core](https://github.com/dequelabs/axe-core)
- [WCAG 2.1 Guidelines](https://www.w3.org/WAI/WCAG21/quickref/)

---

## 🎯 Quick Reference

```bash
# SETUP
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 (Windows)
pip install -r requirements_minimal.txt
playwright install chromium

# RUN TESTS
pytest -v                          # All tests
pytest -m ui -v                    # UI tests only
pytest -m "ui and english" -v      # UI + English
pytest -v -n 4                     # Parallel (4 workers)

# REPORTS
start reports/report.html          # HTML report (Windows)
allure serve reports/allure-results # Allure report

# DEBUGGING
pytest -v -s                       # Show print statements
pytest -v -x                       # Stop on first failure
pytest --lf -v                     # Run last failed

# BY LANGUAGE
pytest -m english -v               # English tests
pytest -m arabic -v                # Arabic tests
pytest -m bilingual -v             # Bilingual tests

# BY CATEGORY
pytest -m accessibility -v         # Accessibility
pytest -m security -v              # Security
pytest -m ai -v                    # AI/RAGAS
```

---

## 📈 Test Statistics

- **Total Tests:** 43
- **Test Files:** 9
- **Page Objects:** 3
- **Test Categories:** 4
- **Languages:** 2 (English, Arabic)
- **Avg Execution Time:** 15-20 minutes (all tests)
- **Parallel Execution:** Supported
- **Pass Rate Target:** ≥95%

---

## 🌟 Key Features Summary

✅ **Easy Setup** - Clear installation steps  
✅ **Multi-language** - English & Arabic with RTL support  
✅ **Comprehensive** - 43 tests across 4 categories  
✅ **Fast** - Parallel execution support  
✅ **Beautiful Reports** - HTML + Allure dashboards  
✅ **Well Documented** - Complete guides and examples  
✅ **CI/CD Ready** - JUnit XML output  
✅ **Maintainable** - Page Object Model architecture  
✅ **Accessible** - WCAG 2.1 Level AA compliance testing  
✅ **Secure** - Comprehensive security testing  
✅ **AI-Powered** - RAGAS metrics for LLM evaluation  

---

**Happy Testing! 🚀**

*For detailed setup instructions and troubleshooting, see [SETUP_GUIDE.md](SETUP_GUIDE.md)*