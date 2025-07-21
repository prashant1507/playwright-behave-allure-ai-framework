# Python Automation Framework with Playwright + Behave + Allure + AI

[![Python](https://img.shields.io/badge/Python-3.12+-blue.svg)](https://python.org)
[![Playwright](https://img.shields.io/badge/Playwright-Latest-green.svg)](https://playwright.dev)
[![Behave](https://img.shields.io/badge/Behave-Latest-orange.svg)](https://behave.readthedocs.io)
[![Allure](https://img.shields.io/badge/Allure-Latest-red.svg)](https://docs.qameta.io/allure/)
[![AI](https://img.shields.io/badge/AI-Ollama-purple.svg)](https://ollama.ai)

A powerful, scalable automation framework combining **Playwright** for browser automation, **Behave** for BDD testing, **Allure** for reporting, **Page Object Model** for maintainable test structure, and **AI-powered selector healing** for robust test automation.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/prashant1507/playwright-behave-allure-framework.git
cd playwright-behave-allure-framework/

# Install dependencies
pip install -r requirements.txt
playwright install

# Install node for checking tracing
brew install node

# Run your first test
python run_tests.py --tags @smoke
```

---

## 📋 Table of Contents

- [✨ Key Features](#-key-features)
- [🏗️ Architecture](#️-architecture)
- [🧠 AI Selector Healing](#-ai-selector-healing)
- [⚙️ Setup Guide](#️-setup-guide)
- [🧪 Running Tests](#-running-tests)
- [📊 Reporting](#-reporting)
- [🏷️ Tag Filtering](#tag-filtering)
- [ Code Organization](#code-organization)
- [🔍 Investigate Tracing](#investigate-tracing)
- [📄 Log Files](#log-files)

---

## ✨ Key Features

| Feature                       | Description                                             | Benefits                                        |
|-------------------------------|---------------------------------------------------------|-------------------------------------------------|
| 🧠 **AI Selector Healing**    | AI-powered selector recovery using Ollama              | Self-healing tests, reduced maintenance         |
| 🏗️ **Page Object Model**     | Centralized element selectors and reusable page methods | Maintainable, scalable test structure           |
| 🚀 **Parallel Execution**     | Multi-worker test execution feature-by-feature          | Faster test execution, efficient resource usage |
| 🏷️ **Smart Tag Filtering**   | Filter tests by tags (`@smoke`, `@regression`, `@api`)  | Run only relevant tests, reduce execution time  |
| 📊 **Enhanced Reporting**     | Allure integration with automatic screenshots           | Detailed HTML reports with failure analysis     |
| ⚙️ **Flexible Configuration** | YAML config + environment variables + command-line args | Easy configuration management                   |
| 🌐 **Multi-Browser Support**  | Chromium, Firefox, WebKit support                       | Cross-browser testing capabilities              |
| 🎯 **Clean Output**           | Filtered console output with organized reporting        | Reduced noise, better debugging                 |

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
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   AI Selector   │    │   Ollama        │    │   Selector      │
│   Healer        │◀──▶│   (AI Model)    │───▶│   Map Cache     │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

---

## 🧠 AI Selector Healing

The framework includes an intelligent **AI-powered selector healing system** that automatically recovers from selector failures using the **Ollama AI model**.

### How It Works

1. **Automatic Detection**: When a selector fails (throws exception), the system automatically triggers AI healing
2. **Context Capture**: Captures current page screenshot and HTML content
3. **AI Analysis**: Uses Ollama (`devstral:24b` model) to analyze the page and suggest new selectors
4. **Validation**: Validates AI-suggested selectors before using them
5. **Learning**: Maintains a `selector_map.json` file for future reference

### Features

- **🧠 Intelligent Recovery**: AI analyzes page structure and suggests optimal selectors
- **📸 Visual Analysis**: Uses screenshots for better element identification
- **🎯 Confidence Scoring**: AI provides confidence levels for suggested selectors
- **📚 Historical Learning**: Maintains selector mapping for reuse and learning
- **🔍 Multiple Selector Types**: Supports XPath, CSS, and text-based selectors
- **⚡ Automatic Integration**: Seamlessly integrated into Page Object Model

### Example Usage

```python
# In base_page.py - Automatic AI healing
def fill_input(self, selector: str, value: str):
    try:
        self.page.locator(selector).wait_for(timeout=5000)
        self.page.fill(selector, value)
    except playwright.sync_api.TimeoutError:
        # AI healing automatically triggered
        locator = ai_selector_healing(context=self.context, text=selector)
        locator.fill(value)
```
### Benefits

- **🔄 Self-Healing Tests**: Tests automatically recover from selector changes
- **📉 Reduced Maintenance**: Less manual selector updates required
- **🎯 Higher Reliability**: AI suggests robust, context-aware selectors
- **📚 Continuous Learning**: Improves over time with historical data
- **⚡ Faster Development**: Reduces debugging time for selector issues

### Note
- AI method is ready, requires user to adjust base_page.py functions

---

## ⚙️ Setup Guide

### 1. Prerequisites

- **Python 3.12+**
- **Git** (for version control)
- **Allure** (for reporting)
- **Ollama** (for AI models)

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

### 5. Install Ollama (Required for AI Selector Healing)

```bash
# Install Ollama
https://ollama.ai/

# Pull the required model
ollama pull devstral:24b
```

### 6. Configuration

#### Set URL in [Config.yaml](resources/config.yaml):

```yaml
base_url: https://httpbin.org
```

**Important:** The `base_url` is **required** in `config.yaml`. The framework will raise an error if it's missing.

#### AI Selector Healing Configuration

The AI selector healing system is automatically configured and ready to use. It will:

- Create `selector_map.json` for historical selector mapping
- Generate `selector_log.json` for AI interaction logs
- Capture screenshots in `reports/screenshots/` for AI analysis
- Use the `devstral:24b` Ollama model by default

### 7. Verify Installation

```bash
# Run a quick test
python run_tests.py --tags @smoke --headless
```

**Note:** The AI selector healing will automatically activate when selectors fail. You can monitor AI interactions in the console output and check the generated logs.

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

# Run with tracing
python run_tests.py --tracing
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

### Investigate Tracing
```bash
# Install Playwright trace viewer
npx playwright show-trace reports/traces/FILE_NAME.zip

# Or use the web interface
npx playwright show-trace --host 0.0.0.0 --port 8080 reports/traces/FILE_NAME.zip
```
---

### Log Files

Check log files for detailed error information:

- `reports/test.log` - Detailed test execution logs
- `reports/workers/` - Parallel execution logs
- `reports/traces/` - Tracing reports

### AI Selector Healing Logs

Monitor AI selector healing activities:

- `selector_map.json` - Historical selector mappings and AI suggestions
- `selector_log.json` - Detailed AI interaction logs with confidence scores
- `reports/screenshots/ai-*.png` - Screenshots captured for AI analysis
- Console output - Real-time AI healing notifications with emojis

---

*Built with ❤️ using Python, Playwright, Behave, Allure, and AI-powered selector healing*
