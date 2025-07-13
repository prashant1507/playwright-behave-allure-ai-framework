import os

from utils.logger import log_info_emoji


def create_reports_structure():
    folders = [
        "reports",
        "reports/screenshots",
        "reports/workers",
        "reports/allure-results"
    ]

    for folder in folders:
        os.makedirs(folder, exist_ok=True)

    if not hasattr(create_reports_structure, '_shown'):
        log_info_emoji("📁", "Reports structure created")
        create_reports_structure._shown = True