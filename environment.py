import os
import yaml
from playwright_config.browser_setup import BrowserManager
from utils.logger import log_failure, log_warning

def load_config():
    """Load configuration from config.yaml"""
    config_path = os.path.join(os.path.dirname(__file__), 'config.yaml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}

def get_base_url():
    config = load_config()
    if 'base_url' not in config:
        raise ValueError("base_url is missing in config.yaml!")
    return config['base_url']

def build_url(base_url, path=""):
    """Build full URL by combining base_url and path"""
    if path.startswith('/'):
        path = path[1:]  # Remove leading slash
    return f"{base_url}/{path}" if path else base_url

def get_browser_config():
    """Get browser configuration from environment variables (BROWSER and HEADLESS)."""
    browser_type = os.getenv("BROWSER", "chromium").lower()
    headless_env = os.getenv("HEADLESS", "False").lower()
    headless = headless_env in ["true", "1", "yes", "on"]
    return browser_type, headless

def before_all(context):
    # Get browser configuration
    browser_type, headless = get_browser_config()
    context.browser_manager = BrowserManager(browser_type=browser_type, headless=headless)
    context.page = context.browser_manager.start()
    context.base_url = get_base_url()
    context.build_url = build_url

    # Initialize page factory
    from pages.page_factory import PageFactory
    context.page_factory = PageFactory()

def after_all(context):
    context.browser_manager.stop()

def after_step(context, step):
    if step.status == "failed":
        log_failure(f"Step failed: {step.name}")
        if hasattr(context, "page"):
            screenshots_dir = os.path.join("reports", "screenshots")
            os.makedirs(screenshots_dir, exist_ok=True)
            scenario_name = getattr(context, 'scenario', None)
            scenario_name = scenario_name.name.replace(' ', '_').replace('/', '_') if scenario_name else 'unknown_scenario'
            step_name = step.name.replace(' ', '_').replace('/', '_')
            screenshot_path = os.path.join(screenshots_dir, f"screenshot_{scenario_name}_{step_name}.png")
            context.page.screenshot(path=screenshot_path)
            # Attach to Allure if available
            try:
                import allure
                with open(screenshot_path, "rb") as image_file:
                    allure.attach(
                        image_file.read(),
                        name=f"screenshot_{scenario_name}_{step_name}",
                        attachment_type=allure.attachment_type.PNG
                    )
            except ImportError:
                log_warning("Allure not available, screenshot not attached to report.")
            except Exception as e:
                log_failure(f"Failed to attach screenshot to Allure: {e}")