import time
from playwright.sync_api import sync_playwright

from helpers.constants.framework_constants import TRACES_VIDEOS_DIR, TRACES_DIR
from utils.logger import log_info
from utils.playwright_config.trace_manager import TraceManager


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