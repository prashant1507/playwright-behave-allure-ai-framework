import os

from helpers.constants.framework_constants import CONFIG_YAML
from utils.misc import load_config
import time
from playwright.sync_api import sync_playwright

from helpers.constants.framework_constants import TRACES_VIDEOS_DIR, TRACES_DIR
from utils.logger import log_info
from utils.browser.trace_manager import TraceManager


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

class BrowserManager:
    def __init__(self, browser_type="chromium", headless=False, enable_tracing=False):
        self.playwright = None
        self.browser = None
        self.page = None
        self.headless = headless
        self.browser_type = browser_type
        self.enable_tracing = enable_tracing
        self.context = None
        self.trace_manager = TraceManager(self.enable_tracing)

    def start(self):
        if self.enable_tracing:
            self.trace_manager.archive_old_traces()
        self.playwright = sync_playwright().start()
        browser_launcher = getattr(self.playwright, self.browser_type)
        self.browser = browser_launcher.launch(headless=self.headless)
        if self.enable_tracing:
            self.context = self.browser.new_context(
                record_video_dir=TRACES_VIDEOS_DIR if self.enable_tracing else None,
                record_har_path=f"{TRACES_DIR}/har" if self.enable_tracing else None
            )
            self.context.tracing.start(screenshots=True, snapshots=True, sources=True)
        else:
            self.context = self.browser.new_context()

        self.page = self.context.new_page()
        return self.page

    def stop(self):
        if self.enable_tracing and self.context:
            trace_path = f"{TRACES_DIR}/trace-{self.browser_type}-{int(time.time())}.zip"
            self.context.tracing.stop(path=trace_path)
            log_info(f"Trace saved to: {trace_path}")
            self.trace_manager.cleanup_empty_directories()

        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()