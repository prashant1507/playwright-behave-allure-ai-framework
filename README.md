# Python Automation Framework with Playwright + Behave + Allure

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev)
[![Behave](https://img.shields.io/badge/Behave-Latest-orange.svg)](https://behave.readthedocs.io)
[![Allure](https://img.shields.io/badge/Allure-Latest-red.svg)](https://docs.qameta.io/allure/)

A powerful, scalable automation framework combining **Playwright** for browser automation, **Behave** for BDD testing, *
*Allure** for reporting, and **Page Object Model** for maintainable test structure.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/prashant1507/playwright-behave-allure-framework.git
cd playwright-behave-allure-framework/

# Install dependencies
pip install -r requirements.txt
playwright install

# Run your first test
python run_tests.py --tags @smoke
```

---

## 📋 Table of Contents

- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [📦 Project Structure](#-project-structure)
- [⚙️ Setup Guide](#️-setup-guide)
- [🧪 Running Tests](#-running-tests)
- [📊 Reporting](#-reporting)
- [🏷️ Tag Filtering](#tag-filtering)
- [�� Code Organization](#code-organization)
- [📄 Log Files](#log-files)

---

## ✨ Key Features

| Feature                       | Description                                                | Benefits                                        |
|-------------------------------|------------------------------------------------------------|-------------------------------------------------|
| 🏗️ **Page Object Model**     | Centralized element selectors and reusable page methods    | Maintainable, scalable test structure           |
| 🚀 **Parallel Execution**     | Multi-worker test execution with smart resource management | Faster test execution, efficient resource usage |
| 🏷️ **Smart Tag Filtering**   | Filter tests by tags (`@smoke`, `@regression`, `@api`)     | Run only relevant tests, reduce execution time  |
| 📊 **Enhanced Reporting**     | Allure integration with automatic screenshots              | Detailed HTML reports with failure analysis     |
| ⚙️ **Flexible Configuration** | YAML config + environment variables + command-line args    | Easy configuration management                   |
| 🌐 **Multi-Browser Support**  | Chromium, Firefox, WebKit support                          | Cross-browser testing capabilities              |
| 🎯 **Clean Output**           | Filtered console output with organized reporting           | Reduced noise, better debugging                 |

---

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Feature Files │    │  Step Defs      │    │  Page Objects   │
│   (Gherkin)     │───▶│  (Test Logic)   │───▶│  (Selectors)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Behave        │    │   Playwright    │    │   Allure        │
│   (BDD Engine)  │    │   (Browser)     │    │   (Reporting)   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 📦 Project Structure

```
project-root/
├── 📁 features/                  # Gherkin feature files
│   ├── login.feature             # Login functionality tests
│   ├── ...
│
├── 📁 steps/                     # Behave step definitions
│   ├── login_steps.py            # Login step implementations
│   ├── ...
│
├── 📁 pages/                     # Page Object Model
│   ├── __init__.py               # Package initialization
│   ├── base_page.py              # Base page with common methods
│   ├── test_page.py              # Test page interactions
│   ├── page_factory.py           # Page object factory
│   └── ...
│
├── 📁 playwright_config/         # Playwright configuration
│   └── browser_setup.py          # Browser setup and management
│
├── 📁 reports/                   # Test reports and artifacts
│   ├── allure-results/           # Allure report data
│   ├── screenshots/              # Failure screenshots
│   └── workers/                  # Parallel execution logs
│
├── ⚙️ environment.py             # Behave hooks and setup
├── ⚙️ behave.ini                 # Behave configuration
├── ⚙️ config.yaml                # Application configuration
├── 🚀 run_tests.py               # Enhanced test runner
├── 📋 requirements.txt           # Python dependencies
├── 📋 .gitignore                 # Git ignore rules
└── 📖 README.md                  # This file
```

---

## ⚙️ Setup Guide

### 1. Prerequisites

- **Python 3.12+**
- **Git** (for version control)
- **Allure** (for reporting)

### 2. Environment Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 3. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install Playwright browsers
playwright install
```

### 4. Install Allure (Optional)

```bash
# macOS (using Homebrew)
brew install allure

# Windows (using Scoop)
scoop install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

### 5. Configuration

#### Set URL in `config.yaml`:

```yaml
base_url: https://httpbin.org
```

**Important:** The `base_url` is **required** in `config.yaml`. The framework will raise an error if it's missing.

### 6. Verify Installation

```bash
# Run a quick test
python run_tests.py --tags @smoke --headless
```

---

## 🧪 Running Tests

### Basic Test Execution

```bash
# Run all tests
python run_tests.py

# Run specific feature files
python run_tests.py features/login.feature features/forms.feature

# Run tagged tests
python run_tests.py --tags @smoke
python run_tests.py --tags @regression
```

### Parallel Execution

```bash
# Run with optimal worker count
python run_tests.py --parallel

# Run with custom workers
python run_tests.py --parallel --workers 4

# Run tagged tests in parallel
python run_tests.py --parallel --tags @smoke @regression
```

### Browser Options

```bash
# Different browsers
python run_tests.py --browser chromium
python run_tests.py --browser firefox
python run_tests.py --browser webkit

# Headless mode
python run_tests.py --headless
python run_tests.py --browser firefox --headless
```

### Advanced Combinations

```bash
# Parallel execution with specific browser and headless mode
python run_tests.py --parallel --browser firefox --headless --workers 4

# Run specific tags with custom configuration
python run_tests.py --tags @smoke @api --browser webkit --headless

# Run with auto-serve report
python run_tests.py --tags @smoke --serve-report
```

---

## 📊 Reporting

### Allure Reports

```bash
# Generate and serve report
python run_tests.py --tags @smoke --serve-report

# Or manually serve existing report
allure serve reports/allure-results
```

### Report Features

- **📊 HTML Reports** - Detailed test results with trends
- **📸 Screenshots** - Automatic capture on failures
- **📋 Failing Scenarios** - Clear summary of failed tests
- **📈 Trends** - Historical test execution data
- **🔍 Detailed Analysis** - Step-by-step failure analysis

### Report Structure

```
reports/
├── allure-results/          # Allure report data
│   ├── *.json               # Test results
│   └── *.xml                # Test metadata
├── screenshots/             # Failure screenshots
│   └── screenshot_*.png     # Automatic screenshots
└── workers/                 # Parallel execution logs
    └── worker_*.log         # Worker-specific logs
```

### Best Practices

1. **Keep selectors in page objects** - Centralized element management
2. **Keep assertions in step definitions** - Test logic separation
3. **Use Playwright's `expect()`** - Reliable assertions
4. **Create reusable page methods** - Reduce code duplication

--- 
## Tag Filtering

Available tags in the framework:

- `@smoke` - Quick validation tests
- `@regression` - Comprehensive test suite
- `@api` - API testing scenarios
- `@performance` - Performance testing

```bash
# Single tag
python run_tests.py --tags @smoke

# Multiple tags (OR logic)
python run_tests.py --tags @smoke @regression

# Parallel with tags
python run_tests.py --parallel --tags @api
```

---

### Code Organization

1. **Keep step definitions focused**
   ```python
   @when("the user clicks the login button")
   def step_click_login(context):
       login_page = context.page_factory.get_login_page(context.page)
       login_page.click_login_button()
   ```

2. **Use page objects for interactions**
   ```python
   def click_login_button(self):
       self.click_element(self.LOGIN_BUTTON)
   ```

3. **Use Playwright assertions**
   ```python
   expect(context.page).to_contain_text("Welcome")
   ```

---

### Log Files

Check log files for detailed error information:

- `reports/test.log` - Detailed test execution logs
- `reports/workers/` - Parallel execution logs

---

*Built with ❤️ using Python, Playwright, Behave, and Allure*
