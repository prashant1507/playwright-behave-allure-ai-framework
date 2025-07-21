import os

from helpers.constants.framework_constants import SCREENSHOTS_DIR, REPORTS, WORKER_DIR, ALLURE_RESULTS_DIR
from utils.logger import log_info_emoji


def create_reports_structure():
    folders = [
        REPORTS,
        SCREENSHOTS_DIR,
        WORKER_DIR,
        ALLURE_RESULTS_DIR
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    if not hasattr(create_reports_structure, '_shown'):
        log_info_emoji("📁", "Reports structure created")
        create_reports_structure._shown = True