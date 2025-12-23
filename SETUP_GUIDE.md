# 🚀 U-ASK TEST FRAMEWORK - SETUP GUIDE

Complete step-by-step setup instructions for installing and configuring the test automation framework.

---

## 📋 TABLE OF CONTENTS

1. [Prerequisites](#prerequisites)
2. [Quick Start](#quick-start)
3. [Detailed Installation](#detailed-installation)
4. [Configuration](#configuration)
5. [Verification](#verification)
6. [Troubleshooting](#troubleshooting)
7. [Advanced Setup](#advanced-setup)
8. [FAQ](#faq)

---

## 📋 PREREQUISITES

### System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|-------------|
| **OS** | Windows 10, macOS 11, Ubuntu 20.04 | Windows 11, macOS 13, Ubuntu 22.04 |
| **RAM** | 8 GB | 16 GB |
| **Disk Space** | 5 GB free | 10 GB free |
| **Internet** | Broadband | Broadband |

### Required Software

| Software | Version | Download Link | Purpose |
|----------|---------|---------------|---------|
| **Python** | 3.12+ | https://www.python.org/downloads/ | Core runtime |
| **Git** | Latest | https://git-scm.com/downloads | Source control |
| **Code Editor** | Any | VS Code, PyCharm, etc. | Development |

### Optional Software

| Software | Purpose | Installation |
|----------|---------|--------------|
| **Allure CLI** | Report generation | See [Step 6](#step-6-install-allure-cli-optional) |
| **Scoop** (Windows) | Package manager | https://scoop.sh |
| **Homebrew** (Mac) | Package manager | https://brew.sh |

---

## 🚀 QUICK START

### One-Command Setup

Choose your operating system:

#### Windows (PowerShell):
```powershell
# 1. Clone repository
git clone <repository-url>
cd perplexity

# 2. Create and activate virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements_minimal.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# 6. Run first test
pytest -v -k "test_chat_widget_loads_desktop"
```

#### Linux/Mac:
```bash
# 1. Clone repository
git clone <repository-url>
cd perplexity

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements_minimal.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"

# 6. Run first test
pytest -v -k "test_chat_widget_loads_desktop"
```

**🎉 If the test runs successfully, you're all set! Skip to [Running Tests](#8-running-tests).**

---

## 🔧 DETAILED INSTALLATION

Follow these steps if quick start didn't work or you prefer manual setup.

### Step 1: Verify Python Installation

#### Check Python Version:
```bash
python --version
# Expected: Python 3.12.x or higher

# On Mac/Linux, may need:
python3 --version
```

#### If Python is not installed or version is < 3.12:

**Windows:**
1. Download from https://www.python.org/downloads/
2. Run installer
3. ✅ **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Restart terminal/PowerShell

**Mac:**
```bash
# Using Homebrew
brew install python@3.12
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3.12 python3.12-venv python3-pip
```

#### Verify Installation:
```bash
python --version  # or python3 --version
pip --version     # or pip3 --version
```

---

### Step 2: Clone the Repository

```bash
# Navigate to your projects folder
cd ~/projects  # or C:\Users\YourName\projects on Windows

# Clone repository
git clone <repository-url>

# Navigate into project
cd perplexity

# Verify you're in the right place
ls
# Should see: conftest.py, pytest.ini, tests/, pages/, etc.
```

#### If you don't have Git:

**Windows:**
- Download from https://git-scm.com/downloads
- Install with default settings

**Mac:**
```bash
# Git comes with Xcode Command Line Tools
xcode-select --install
```

**Linux:**
```bash
sudo apt install git
```

---

### Step 3: Create Virtual Environment

#### Why Virtual Environment?
- ✅ Isolates project dependencies
- ✅ Prevents version conflicts with other projects
- ✅ Easy to recreate if something breaks
- ✅ Safe to delete and start fresh

#### Windows (PowerShell):
```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
# Then try activating again
```

#### Windows (CMD):
```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate.bat
```

#### Mac/Linux:
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Verify activation (should show venv path)
which python
```

#### Success Indicator:
Your prompt should now show `(venv)` at the beginning:
```
(venv) C:\projects\perplexity>    # Windows
(venv) ~/projects/perplexity$     # Linux/Mac
```

---

### Step 4: Install Python Dependencies

#### Option A: Minimal Installation (RECOMMENDED) ⭐

**Best for:** Most users, quick setup, standard testing

```bash
# Upgrade pip first
pip install --upgrade pip

# Install minimal dependencies
pip install -r requirements_minimal.txt

# This installs ~25 core packages
```

**Packages installed:**
- pytest, pytest-playwright, pytest-html, pytest-xdist
- playwright
- allure-pytest
- pyyaml, python-dotenv
- axe-playwright-python
- langchain-openai, langchain-huggingface
- ragas
- sentence-transformers, transformers, torch
- nltk
- requests, nest-asyncio

**Installation time:** 2-5 minutes  
**Disk space:** ~500 MB

---

#### Option B: Full Installation (All Features)

**Best for:** Production use, document processing, complete feature set

```bash
# Upgrade pip first
pip install --upgrade pip

# Install all dependencies
pip install -r requirements_verified.txt

# This installs ~150 packages
```

**Additional packages:**
- Document processing (docx, pdf, etc.)
- Advanced NLP libraries
- Additional AI/ML tools
- Development utilities

**Installation time:** 10-20 minutes  
**Disk space:** ~2 GB

---

#### Verify Installation:
```bash
# Check key packages
pip list | grep pytest
pip list | grep playwright
pip list | grep ragas

# Or view all installed packages
pip list
```

---

### Step 5: Install Playwright Browsers

Playwright needs to download browser binaries:

```bash
# Install Chromium (required)
playwright install chromium

# Installation takes 2-5 minutes
# Downloads ~200 MB
```

#### Verify Installation:
```bash
# Check Playwright version
playwright --version

# List installed browsers
playwright show-browsers
```

#### If installation fails:
```bash
# Try with Python module prefix
python -m playwright install chromium

# Or install all browsers
playwright install
```

---

### Step 6: Install Allure CLI (Optional)

Allure provides interactive test reports. **This is optional** - tests will work without it.

#### Windows (using Scoop):
```powershell
# Install Scoop first if not installed
iwr -useb get.scoop.sh | iex

# Install Allure
scoop install allure

# Verify installation
allure --version
```

#### Mac (using Homebrew):
```bash
# Install Allure
brew install allure

# Verify installation
allure --version
```

#### Linux (Ubuntu/Debian):
```bash
# Install Java (required for Allure)
sudo apt-get update
sudo apt-get install default-jre

# Add Allure repository
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update

# Install Allure
sudo apt-get install allure

# Verify installation
allure --version
```

#### Manual Installation (All OS):
```bash
# Download from: https://github.com/allure-framework/allure2/releases
# Extract to a folder
# Add to system PATH
```

**Note:** If you skip this step, you can still view HTML reports (reports/report.html)

---

### Step 7: Download NLTK Data

NLTK (Natural Language Toolkit) is used for AI tests and requires additional data files:

```bash
# Download required NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
```

#### Or use interactive Python:
```python
python
>>> import nltk
>>> nltk.download('punkt')
>>> nltk.download('averaged_perceptron_tagger')
>>> exit()
```

#### Verify:
```bash
# Check if NLTK data exists
ls nltk_data/tokenizers/punkt_tab/  # Should show language folders
ls nltk_data/taggers/  # Should show averaged_perceptron_tagger_eng/
```

---

### Step 8: Running Tests

#### First Test Run:
```bash
# Run a single UI test to verify setup
pytest tests/ui/test_chat_ui.py::test_chat_widget_loads_desktop -v -s

# Expected output:
# tests/ui/test_chat_ui.py::test_chat_widget_loads_desktop PASSED
```

#### If test passes: ✅ **Setup Complete!**

#### If test fails: See [Troubleshooting](#troubleshooting)

---

## ⚙️ CONFIGURATION

### config.yaml

Located at: `config/config.yaml`

This file contains all framework settings:

```yaml
# Application URL
base_url: "https://govgpt.sandbox.dge.gov.ae/"

# Test Credentials
username: "qatest1@dge.gov.ae"
password: "DGEUser100!"

# Language Settings
default_language: "en"  # "en" or "ar"

# Timeout Settings
timeout_ms: 60000  # 60 seconds (increase if tests timeout)

# API Keys (can also use .env file)
openApiKey: "sk-proj-..."           # OpenAI API key
PERPLEXITY_API_KEY: "pplx-..."      # Perplexity API key
RAGA_APP_TOKEN: ""                  # RAGA token (optional)

# Video Recording (optional)
enable_video_recording: false  # Set to true to record test execution
video_dir: "videos/"           # Directory to save videos
```

#### How to Modify:

**1. Open file in editor:**
```bash
# Windows:
notepad config/config.yaml

# Mac/Linux:
nano config/config.yaml
# or
code config/config.yaml  # VS Code
```

**2. Edit settings as needed**

**3. Save and close**

---

### .env File (Recommended for API Keys)

Create a `.env` file in project root for sensitive data:

```bash
# Create .env file
# Windows (PowerShell):
New-Item -Path .env -ItemType File

# Linux/Mac:
touch .env
```

**Add API keys:**
```env
PERPLEXITY_API_KEY=your-perplexity-api-key-here
openApiKey=your-openai-api-key-here
```

**Benefits:**
- ✅ Keeps sensitive data out of version control
- ✅ Easy to share config without exposing keys
- ✅ Can override config.yaml settings

**Note:** `.env` values take precedence over `config.yaml`

---

### pytest.ini

Located at: `pytest.ini`

Controls pytest behavior. **You typically don't need to modify this.**

```ini
[pytest]
# Test markers for categorization
markers =
    accessibility: Accessibility tests
    ai: AI/RAGAS tests
    security: Security tests
    ui: UI functional tests
    english: English language tests
    arabic: Arabic language tests
    bilingual: Multi-language tests
    slow: Slow running tests
    smoke: Smoke tests
    mobile: Mobile device tests
    ragas: RAGAS evaluation tests

# Default pytest options
addopts =
    --html=reports/report.html       # HTML report location
    --self-contained-html            # Single file report
    --alluredir=reports/allure-results  # Allure results location
    --clean-alluredir                # Clean old Allure results
    -v                                # Verbose output

# Test discovery
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

---

## ✅ VERIFICATION

### Verify Complete Setup

Run these commands to ensure everything is installed correctly:

#### 1. Check Virtual Environment:
```bash
# Should show (venv) in prompt
# Windows:
Get-Command python | Select-Object Source
# Should show: C:\...\perplexity\venv\Scripts\python.exe

# Linux/Mac:
which python
# Should show: .../perplexity/venv/bin/python
```

#### 2. Check Python Packages:
```bash
pip list | grep -E "pytest|playwright|allure|ragas"

# Expected output (versions may vary):
# allure-pytest        2.15.2
# axe-playwright-python 0.1.7
# playwright           1.57.0
# pytest               8.4.2
# pytest-html          4.1.1
# pytest-playwright    0.7.2
# pytest-xdist         3.8.0
# ragas                0.4.1
```

#### 3. Check Playwright Browsers:
```bash
playwright show-browsers

# Expected output:
# chromium 1147 (latest)
```

#### 4. Check NLTK Data:
```bash
# Windows:
dir nltk_data\tokenizers\punkt_tab
dir nltk_data\taggers

# Linux/Mac:
ls -la nltk_data/tokenizers/punkt_tab/
ls -la nltk_data/taggers/
```

#### 5. Check Allure (Optional):
```bash
allure --version

# Expected output:
# 2.x.x (any version)
```

#### 6. Run Smoke Test:
```bash
# Run a quick test to verify everything works
pytest -m smoke -v

# Or run single UI test:
pytest tests/ui/test_chat_ui.py::test_chat_widget_loads_desktop -v -s
```

#### 7. Check Report Generation:
```bash
# After running tests, check if reports were created:
# Windows:
dir reports

# Linux/Mac:
ls -la reports/

# Should see:
# report.html           (pytest-html report)
# allure-results/       (Allure results)
# axe_chat_page.json   (axe accessibility report)
```

### ✅ Success Indicators

If all of the above work, you should see:
- ✅ (venv) in terminal prompt
- ✅ pytest, playwright, ragas installed
- ✅ Chromium browser installed
- ✅ NLTK data downloaded
- ✅ Tests run successfully
- ✅ Reports generated

**🎉 Setup Complete! You're ready to run tests!**

---

## 🐛 TROUBLESHOOTING

### Common Issues and Solutions

#### Issue 1: Python Command Not Found

**Symptoms:**
```bash
'python' is not recognized as an internal or external command
```

**Solution:**
```bash
# Windows: Reinstall Python and check "Add Python to PATH"
# Or use: python3 --version

# Mac/Linux: Use python3 instead of python
python3 --version
pip3 install -r requirements_minimal.txt
```

---

#### Issue 2: Virtual Environment Activation Fails (Windows)

**Symptoms:**
```powershell
.\venv\Scripts\Activate.ps1 : ... execution of scripts is disabled on this system
```

**Solution:**
```powershell
# Allow script execution for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then activate again
.\venv\Scripts\Activate.ps1

# Verify (venv) appears in prompt
```

---

#### Issue 3: pip install fails with Permission Error

**Symptoms:**
```bash
ERROR: Could not install packages due to an OSError: [Errno 13] Permission denied
```

**Solution:**
```bash
# Option 1: Use --user flag (not recommended in venv)
pip install --user -r requirements_minimal.txt

# Option 2: Check if venv is activated
# Should see (venv) in prompt

# Option 3: Recreate virtual environment
deactivate  # if already activated
rm -rf venv  # or rmdir /s venv (Windows CMD)
python -m venv venv
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1 (Windows)
pip install -r requirements_minimal.txt
```

---

#### Issue 4: Playwright Install Fails

**Symptoms:**
```bash
playwright install chromium
# Fails with download error
```

**Solution:**
```bash
# Option 1: Use Python module prefix
python -m playwright install chromium

# Option 2: Install with dependencies
playwright install chromium --with-deps

# Option 3: Manual download (last resort)
# Check network/firewall settings
# Try from different network
```

---

#### Issue 5: NLTK Download Fails

**Symptoms:**
```bash
python -c "import nltk; nltk.download('punkt')"
# SSL Error or timeout
```

**Solution:**
```bash
# Option 1: Use interactive mode
python
>>> import nltk
>>> import ssl
>>> ssl._create_default_https_context = ssl._create_unverified_context
>>> nltk.download('punkt')
>>> nltk.download('averaged_perceptron_tagger')
>>> exit()

# Option 2: The framework already includes nltk_data folder
# Just verify it exists:
ls nltk_data/
```

---

#### Issue 6: Tests Timeout

**Symptoms:**
```bash
playwright._impl._api_types.TimeoutError: Timeout 60000ms exceeded
```

**Solution:**
```yaml
# Edit config/config.yaml and increase timeout:
timeout_ms: 120000  # Increase from 60000 to 120000 (2 minutes)

# Or check:
# 1. Internet connection
# 2. Application URL is accessible
# 3. Credentials are correct
```

---

#### Issue 7: Import Errors After Installation

**Symptoms:**
```bash
ImportError: No module named 'playwright'
ModuleNotFoundError: No module named 'pytest'
```

**Solution:**
```bash
# 1. Verify virtual environment is activated
# Should see (venv) in prompt

# 2. If not activated:
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 3. Reinstall dependencies
pip install -r requirements_minimal.txt

# 4. Verify installation
pip list | grep playwright
```

---

#### Issue 8: Allure Command Not Found

**Symptoms:**
```bash
allure: command not found
'allure' is not recognized
```

**Solution:**

**Windows:**
```powershell
# Install Scoop (package manager)
iwr -useb get.scoop.sh | iex

# Install Allure
scoop install allure

# Verify
allure --version
```

**Mac:**
```bash
# Install Homebrew if not installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Allure
brew install allure

# Verify
allure --version
```

**Linux:**
```bash
# Install Java first
sudo apt-get update
sudo apt-get install default-jre

# Add Allure repository
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure

# Verify
allure --version
```

**Note:** Allure is optional - you can still use HTML reports without it.

---

#### Issue 9: Tests Pass But No Reports Generated

**Symptoms:**
- Tests run successfully
- No report.html in reports/ folder
- No allure-results/ folder

**Solution:**
```bash
# 1. Check pytest.ini has reporting options:
cat pytest.ini | grep "addopts"

# Should see:
# --html=reports/report.html
# --alluredir=reports/allure-results

# 2. Ensure reports directory exists:
mkdir -p reports

# 3. Run tests again:
pytest -v

# 4. Check for reports:
ls reports/
```

---

#### Issue 10: API Key Errors in AI Tests

**Symptoms:**
```bash
ValueError: PERPLEXITY_API_KEY not found
AuthenticationError: Incorrect API key
```

**Solution:**

**Option 1: Use config.yaml**
```yaml
# Edit config/config.yaml
PERPLEXITY_API_KEY: "your-actual-key-here"
openApiKey: "your-openai-key-here"
```

**Option 2: Use .env file (Recommended)**
```bash
# Create .env file in project root
echo "PERPLEXITY_API_KEY=your-key-here" > .env
echo "openApiKey=your-key-here" >> .env
```

**Option 3: Skip AI tests**
```bash
# Run tests without AI category
pytest -m "not ai" -v
```

---

#### Issue 11: Video Recording Not Working

**Symptoms:**
- enable_video_recording: true in config
- But no videos in videos/ folder

**Solution:**
```bash
# 1. Ensure videos directory exists
mkdir videos

# 2. Check config/config.yaml:
enable_video_recording: true  # Must be true
video_dir: "videos/"

# 3. Run a test
pytest tests/ui/test_chat_ui.py::test_user_can_send_message -v

# 4. Check videos folder:
ls videos/
```

---

## 🔬 ADVANCED SETUP

### Setting Up IDE (VS Code)

#### 1. Install VS Code:
Download from: https://code.visualstudio.com/

#### 2. Install Extensions:
- Python (Microsoft)
- Pytest (Microsoft)
- Playwright Test for VSCode

#### 3. Configure Python Interpreter:
```
Ctrl+Shift+P → "Python: Select Interpreter"
→ Choose: ./venv/bin/python (or .\venv\Scripts\python.exe on Windows)
```

#### 4. Configure Test Explorer:
```json
// .vscode/settings.json
{
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["-v"],
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python"
}
```

---

### Setting Up IDE (PyCharm)

#### 1. Open Project:
File → Open → Select perplexity folder

#### 2. Configure Python Interpreter:
```
File → Settings → Project: perplexity → Python Interpreter
→ Add Interpreter → Existing Environment
→ Select: perplexity/venv/bin/python
```

#### 3. Configure Pytest:
```
File → Settings → Tools → Python Integrated Tools
→ Testing: pytest
→ Apply
```

#### 4. Run Configuration:
```
Run → Edit Configurations → + → pytest
Name: All Tests
Target: Custom
Working directory: /path/to/perplexity
```

---

### Parallel Execution Setup

Install pytest-xdist (already in requirements):

```bash
# Already installed, but verify:
pip list | grep pytest-xdist

# Run tests in parallel (4 workers):
pytest -v -n 4

# Auto-detect number of CPUs:
pytest -v -n auto
```

---

### CI/CD Setup (GitHub Actions)

Create `.github/workflows/tests.yml`:

```yaml
name: Test Suite

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      
      - name: Install dependencies
        run: |
          python -m venv venv
          source venv/bin/activate
          pip install --upgrade pip
          pip install -r requirements_minimal.txt
          playwright install chromium
          python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger')"
      
      - name: Run tests
        env:
          PERPLEXITY_API_KEY: ${{ secrets.PERPLEXITY_API_KEY }}
        run: |
          source venv/bin/activate
          pytest -v -n 4 --junitxml=reports/junit.xml
      
      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v3
        with:
          name: test-results
          path: reports/
```

---

## ❓ FAQ

### Q1: Do I need to install all requirements files?

**A:** No. Choose one:
- `requirements_minimal.txt` - For most users (recommended)
- `requirements_verified.txt` - For full features

---

### Q2: Can I run tests without Allure?

**A:** Yes! Allure is optional. You'll still get HTML reports in `reports/report.html`.

---

### Q3: How do I update dependencies?

```bash
# Activate virtual environment
source venv/bin/activate  # or .\venv\Scripts\Activate.ps1

# Update all packages
pip install --upgrade -r requirements_minimal.txt

# Or update specific package
pip install --upgrade pytest
```

---

### Q4: Can I use a different browser?

**A:** Yes. Edit `conftest.py`:

```python
# Find this line:
browser = playwright_instance.chromium.launch(headless=False)

# Change to:
browser = playwright_instance.firefox.launch(headless=False)
# or
browser = playwright_instance.webkit.launch(headless=False)

# Then install that browser:
playwright install firefox
# or
playwright install webkit
```

---

### Q5: How do I run tests headless?

**A:** Edit `conftest.py`:

```python
# Find:
browser = playwright_instance.chromium.launch(headless=False)

# Change to:
browser = playwright_instance.chromium.launch(headless=True)
```

Or run with environment variable:
```bash
# Linux/Mac:
HEADLESS=true pytest -v

# Windows:
$env:HEADLESS="true"; pytest -v
```

---

### Q6: Where are test results stored?

**A:**
- HTML Report: `reports/report.html`
- Allure Results: `reports/allure-results/`
- Axe Report: `reports/axe_chat_page.json`
- Screenshots: `reports/screenshots/`
- Videos: `videos/` (if enabled)
- Logs: `logs/run_YYYYMMDD_HHMMSS.log`

---

### Q7: How do I clean up old test results?

```bash
# Remove all reports
rm -rf reports/*

# Or on Windows:
rmdir /s reports
mkdir reports

# Allure has auto-clean enabled in pytest.ini
```

---

### Q8: Can I change the test timeout?

**A:** Yes. Edit `config/config.yaml`:

```yaml
timeout_ms: 120000  # Increase from 60000 to 120000 (2 minutes)
```

---

### Q9: How do I skip slow tests?

```bash
# Skip tests marked as slow
pytest -m "not slow" -v
```

---

### Q10: How do I add new test credentials?

**A:** Edit `config/config.yaml`:

```yaml
username: "your-new-username"
password: "your-new-password"
```

Or create additional user configs for different environments.

---

## 📞 Support

### Getting Help

1. **Check Troubleshooting Section** - Most issues covered above
2. **Review README.md** - General framework documentation
3. **Check Test Documentation** - TEST_SCENARIOS_SUMMARY.md
4. **Review Logs** - Check `logs/` folder for detailed error messages
5. **Contact Team** - Reach out to test automation team

### Useful Commands for Debugging

```bash
# Show detailed test output
pytest -v -s

# Run single test with full output
pytest tests/ui/test_chat_ui.py::test_user_can_send_message -v -s

# Check installed packages
pip list

# Check Playwright installation
playwright show-browsers

# Verify Python environment
which python  # Linux/Mac
Get-Command python  # Windows PowerShell
```

---

## ✅ Setup Checklist

Use this checklist to track your progress:

- [ ] Python 3.12+ installed
- [ ] Git installed
- [ ] Repository cloned
- [ ] Virtual environment created
- [ ] Virtual environment activated
- [ ] Dependencies installed (requirements_minimal.txt)
- [ ] Playwright browsers installed
- [ ] NLTK data downloaded
- [ ] Allure CLI installed (optional)
- [ ] config.yaml reviewed
- [ ] First test run successfully
- [ ] Reports generated
- [ ] Setup verified

---

**🎉 Congratulations! Your test automation framework is ready!**

Return to [README.md](README.md) for usage instructions.