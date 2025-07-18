from utils.logger import log_failure
from utils.browser.browser import prepare_browser
from utils.reporting import attach_screenshot


def before_all(context):
    prepare_browser(context)
    from pages.page_factory import PageFactory
    context.page_factory = PageFactory()


def after_all(context):
    context.browser_manager.stop()


def after_step(context, step):
    if step.status == "failed":
        log_failure(f"Step failed: {step.name}")
        if hasattr(context, "page"):
            attach_screenshot(context, step)