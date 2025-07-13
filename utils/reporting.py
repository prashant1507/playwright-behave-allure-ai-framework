import os
import shutil
import subprocess

from utils.logger import log_info_emoji


def combine_allure_reports(report_dirs):
    """Combine Allure reports from multiple workers into a single report."""
    main_report_dir = "reports/allure-results"

    # Create the main report directory
    os.makedirs(main_report_dir, exist_ok=True)

    # Copy all results from worker directories to the main directory
    for report_dir in report_dirs:
        if os.path.exists(report_dir):
            for item in os.listdir(report_dir):
                src = os.path.join(report_dir, item)
                dst = os.path.join(main_report_dir, item)
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                elif os.path.isdir(src):
                    shutil.copytree(src, dst, dirs_exist_ok=True)

    log_info_emoji("📊", f"Allure reports combined in: reports/allure-results")
    log_info_emoji("📖", "To view the report: allure serve reports/allure-results")

def server_report(args):
    if args.serve_report:
        log_info_emoji("📊", "Serving Allure report")
        subprocess.run(['allure', 'serve', 'reports/allure-results'])
    else:
        log_info_emoji("📊", "To view the report: allure serve reports/allure-results")