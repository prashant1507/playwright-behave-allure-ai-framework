import os.path

RESOURCES = os.path.join(os.getcwd(), 'resources')
CONFIG_YAML = os.path.join(RESOURCES, 'config.yaml')

REPORTS = os.path.join(os.getcwd(), 'reports')
SCREENSHOTS_DIR = os.path.join(REPORTS, 'screenshots')
WORKER_DIR = os.path.join(REPORTS, 'workers')
ALLURE_RESULTS_DIR = os.path.join(REPORTS, 'allure-results')

# Tracing
TRACES_DIR = os.path.join(REPORTS, "traces")
TRACES_VIDEOS_DIR = os.path.join(TRACES_DIR, "videos")