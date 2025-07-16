import os
import shutil
import subprocess

from utils.logger import log_info_emoji, log_warning, log_failure


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

def attach_screenshot(context, step):
    try:
        import allure
        screenshots_dir = os.path.join("reports", "screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        scenario_name = getattr(context, 'scenario', None)
        scenario_name = scenario_name.name.replace(' ', '_').replace('/', '_') if scenario_name else 'unknown_scenario'
        step_name = step.name.replace(' ', '_').replace('/', '_')

        screenshot_path = os.path.join(screenshots_dir, f"screenshot_{scenario_name}_{step_name}.png")
        context.page.screenshot(path=screenshot_path)
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