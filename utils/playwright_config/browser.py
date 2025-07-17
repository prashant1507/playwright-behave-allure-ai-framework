import os

from helpers.constants.framework_constants import CONFIG_YAML
from utils.playwright_config.browser_setup import BrowserManager
from utils.misc import load_config


def get_browser_config():
    browser_type = os.getenv("BROWSER", "chromium").lower()
    headless_env = os.getenv("HEADLESS", "False").lower()
    headless = headless_env in ["true", "1", "yes", "on"]
    return browser_type, headless

def set_browser(context):
    enable_tracing = os.getenv('ENABLE_TRACING', 'false').lower() == 'true'
    browser_type, headless = get_browser_config()
    context.browser_manager = BrowserManager(browser_type=browser_type, headless=headless, enable_tracing=enable_tracing)
    return context.browser_manager.start()

def get_base_url():
    config = load_config()
    if 'base_url' not in config:
        raise ValueError(f"base_url is missing in {CONFIG_YAML}!")
    return config['base_url']

def build_url(base_url, path=""):
    if path.startswith('/'):
        path = path[1:]
    return f"{base_url}/{path}" if path else base_url

def prepare_browser(context):
    context.page = set_browser(context)
    context.base_url = get_base_url()
    context.build_url = build_url