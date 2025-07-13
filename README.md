# Python Automation Framework with Playwright + Behave + Allure

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev)
[![Behave](https://img.shields.io/badge/Behave-Latest-orange.svg)](https://behave.readthedocs.io)
[![Allure](https://img.shields.io/badge/Allure-Latest-red.svg)](https://docs.qameta.io/allure/)

A powerful, scalable automation framework combining **Playwright** for browser automation, **Behave** for BDD testing, **Allure** for reporting, and **Page Object Model** for maintainable test structure.

## 🚀 Quick Start

```bash
# Clone and setup
git clone <repository>
cd <project-directory>

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
- [🏗️ Page Object Model](#️-page-object-model)
- [🚀 Advanced Features](#-advanced-features)
- [🎯 Best Practices](#-best-practices)
- [🔧 Troubleshooting](#-troubleshooting)

---

## ✨ Key Features

| Feature | Description | Benefits |
|---------|-------------|----------|
| 🏗️ **Page Object Model** | Centralized element selectors and reusable page methods | Maintainable, scalable test structure |
| 🚀 **Parallel Execution** | Multi-worker test execution with smart resource management | Faster test execution, efficient resource usage |
| 🏷️ **Smart Tag Filtering** | Filter tests by tags (`@smoke`, `@regression`, `@api`) | Run only relevant tests, reduce execution time |
| 📊 **Enhanced Reporting** | Allure integration with automatic screenshots | Detailed HTML reports with failure analysis |
| ⚙️ **Flexible Configuration** | YAML config + environment variables + command-line args | Easy configuration management |
| 🌐 **Multi-Browser Support** | Chromium, Firefox, WebKit support | Cross-browser testing capabilities |
| 🎯 **Clean Output** | Filtered console output with organized reporting | Reduced noise, better debugging |

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
├── 📁 features/                    # Gherkin feature files
│   ├── login.feature              # Login functionality tests
│   ├── forms.feature              # Form interaction tests
│   ├── navigation.feature         # Navigation tests
│   ├── api_testing.feature        # API testing scenarios
│   └── performance.feature        # Performance tests
│
├── 📁 steps/                      # Behave step definitions
│   ├── login_steps.py            # Login step implementations
│   ├── forms_steps.py            # Form interaction steps
│   ├── navigation_steps.py       # Navigation steps
│   ├── api_steps.py              # API testing steps
│   └── performance_steps.py      # Performance test steps
│
├── 📁 pages/                      # Page Object Model
│   ├── __init__.py               # Package initialization
│   ├── base_page.py              # Base page with common methods
│   ├── test_page.py              # Test page interactions
│   ├── contact_form_page.py      # Contact form page
│   └── page_factory.py           # Page object factory
│
├── 📁 playwright_config/          # Playwright configuration
│   └── browser_setup.py          # Browser setup and management
│
├── 📁 reports/                    # Test reports and artifacts
│   ├── allure-results/           # Allure report data
│   ├── screenshots/              # Failure screenshots
│   └── workers/                  # Parallel execution logs
│
├── ⚙️ environment.py              # Behave hooks and setup
├── ⚙️ behave.ini                  # Behave configuration
├── ⚙️ config.yaml                 # Application configuration
├── 🚀 run_tests.py               # Enhanced test runner
├── 📋 requirements.txt            # Python dependencies
├── 📋 .gitignore                  # Git ignore rules
└── 📖 README.md                   # This file
```

---

## ⚙️ Setup Guide

### 1. Prerequisites

- **Python 3.8+**
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

#### Create `config.yaml`:
```yaml
base_url: https://httpbin.org
```

#### Create `behave.ini`:
```ini
[behave]
show_skipped = false
```

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

### Environment Variables

```bash
# Set environment variables
export HEADLESS=true
export BROWSER=firefox

# Run tests (will use environment variables)
python run_tests.py --tags @smoke
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
├── allure-results/           # Allure report data
│   ├── *.json               # Test results
│   └── *.xml                # Test metadata
├── screenshots/              # Failure screenshots
│   └── screenshot_*.png     # Automatic screenshots
└── workers/                  # Parallel execution logs
    └── worker_*.log         # Worker-specific logs
```

---

## 🏗️ Page Object Model

### Structure Overview

The framework uses Page Object Model (POM) for maintainable test structure:

```python
# pages/base_page.py - Common functionality
class BasePage:
    def __init__(self, page):
        self.page = page
    
    def click_element(self, selector):
        self.page.click(selector)
    
    def fill_input(self, selector, value):
        self.page.fill(selector, value)

# pages/contact_form_page.py - Specific page
class ContactFormPage(BasePage):
    CUSTOMER_NAME_INPUT = 'input[name="custname"]'
    SUBMIT_BUTTON = 'input[type="submit"]'
    
    def fill_form_with_valid_data(self):
        self.fill_input(self.CUSTOMER_NAME_INPUT, "John Doe")
        self.click_element(self.SUBMIT_BUTTON)

# steps/forms_steps.py - Test logic
@when("the user fills out the contact form with valid data")
def step_fill_contact_form_valid(context):
    contact_form = context.page_factory.get_contact_form_page(context.page)
    contact_form.fill_form_with_valid_data()
    
    # Use Playwright assertions
    expect(context.page).to_contain_text("Form submitted")
```

### Best Practices

1. **Keep selectors in page objects** - Centralized element management
2. **Keep assertions in step definitions** - Test logic separation
3. **Use Playwright's `expect()`** - Reliable assertions
4. **Create reusable page methods** - Reduce code duplication

---

## 🚀 Advanced Features

### Parallel Execution

```bash
# Smart parallel execution
python run_tests.py --parallel --tags @smoke

# Benefits:
# - Only opens browsers for relevant feature files
# - Automatic worker count optimization
# - Combined Allure reports
# - Clean console output
```

### Tag Filtering

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

### Configuration Management

#### YAML Configuration (`config.yaml`)
```yaml
base_url: https://httpbin.org
```

#### Environment Variables
```bash
export HEADLESS=true
export BROWSER=firefox
```

#### Command-Line Arguments
```bash
python run_tests.py --browser firefox --headless
```

### Failing Scenarios Display

The framework automatically displays failing scenarios:

```
📋 Failing Scenarios:
----------------------------------------
  • features/forms.feature:4 - Fill out contact form
  • features/navigation.feature:8 - Navigate to different pages
----------------------------------------
```

---

## 🎯 Best Practices

### Test Organization

1. **Use descriptive scenario names**
   ```gherkin
   Scenario: User can successfully log in with valid credentials
   ```

2. **Tag scenarios appropriately**
   ```gherkin
   @smoke @login
   Scenario: Login with valid credentials
   ```

3. **Group related scenarios**
   ```gherkin
   Feature: User Authentication
     As a user
     I want to log in to the application
     So that I can access my account
   ```

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

### Performance Optimization

1. **Use tag filtering for parallel execution**
   ```bash
   python run_tests.py --parallel --tags @smoke
   ```

2. **Monitor worker count**
   ```bash
   python run_tests.py --parallel --workers 4
   ```

3. **Use headless mode for CI/CD**
   ```bash
   python run_tests.py --headless --parallel
   ```

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Browser Not Launching
```bash
# Reinstall Playwright browsers
playwright install
```

#### 2. Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

#### 3. Allure Not Found
```bash
# Install Allure
brew install allure  # macOS
scoop install allure  # Windows
```

#### 4. Parallel Execution Issues
```bash
# Reduce worker count
python run_tests.py --parallel --workers 2
```

### Debug Mode

```bash
# Run with verbose output
python run_tests.py --tags @smoke --headless
```

### Log Files

Check log files for detailed error information:
- `reports/test.log` - Detailed test execution logs
- `reports/workers/` - Parallel execution logs

---

## 📚 Command Reference

### Basic Commands

| Command | Description |
|---------|-------------|
| `python run_tests.py` | Run all tests |
| `python run_tests.py --tags @smoke` | Run smoke tests |
| `python run_tests.py --parallel` | Run tests in parallel |
| `python run_tests.py --headless` | Run in headless mode |

### Advanced Commands

| Command | Description |
|---------|-------------|
| `python run_tests.py --parallel --workers 4` | Parallel with 4 workers |
| `python run_tests.py --browser firefox --headless` | Firefox in headless mode |
| `python run_tests.py --tags @smoke @regression` | Multiple tags |
| `python run_tests.py --serve-report` | Auto-serve Allure report |

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `HEADLESS` | Run in headless mode | `false` |
| `BROWSER` | Browser type | `chromium` |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request


---

## 🎉 What's New

### Latest Features
- ✅ **Page Object Model (POM)** - Maintainable test structure
- ✅ **Parallel Execution** - Multi-worker test execution
- ✅ **Smart Tag Filtering** - Efficient test selection
- ✅ **Enhanced Reporting** - Allure integration with screenshots
- ✅ **Configuration Management** - YAML and environment variables
- ✅ **Failing Scenarios Display** - Clear test failure summary
- ✅ **Clean Console Output** - Filtered and organized output
- ✅ **Multiple Browser Support** - Chromium, Firefox, WebKit
- ✅ **Flexible Headless Mode** - Environment and command-line options
- ✅ **Auto-Serve Reports** - `--serve-report` option

### Framework Benefits
- 🚀 **Fast Execution** - Parallel processing with smart filtering
- 🏗️ **Maintainable** - POM structure with reusable components
- 📊 **Comprehensive Reporting** - Allure integration with detailed analysis
- ⚙️ **Flexible Configuration** - Multiple configuration options
- 🎯 **User-Friendly** - Clean output and intuitive commands

---

## 📞 Support

For questions, issues, or contributions:
- 📧 Create an issue on GitHub
- 📖 Check the documentation
- 🔧 Review troubleshooting section

---

*Built with ❤️ using Python, Playwright, Behave, and Allure*
