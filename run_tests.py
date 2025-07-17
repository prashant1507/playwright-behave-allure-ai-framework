import os
import sys
import subprocess
import multiprocessing
from pathlib import Path

from helpers.constants.framework_constants import TRACES_DIR
from helpers.file_system import create_reports_structure
from utils.prepration import run_options
from utils.logger import (
    log_info, log_warning, log_success, log_failure,
    log_info_emoji
)
from utils.reporting import combine_allure_reports, server_report


def distribute_features(feature_files, max_workers):
    """Distribute feature files across workers."""
    worker_tasks = [[] for _ in range(max_workers)]
    for i, feature_file in enumerate(feature_files):
        worker_tasks[i % max_workers].append(feature_file)
    return worker_tasks


def run_worker_features(feature_files, report_dir, tags=None):
    try:
        cmd = [
            sys.executable, '-m', 'behave',
            '-f', 'allure_behave.formatter:AllureFormatter',
            '-o', report_dir,
            '--no-capture',
            '--no-capture-stderr'
        ]
        if tags:
            for tag in tags:
                cmd.extend(['-t', tag])
        cmd += [str(f) for f in feature_files]

        # Stream output, filter empty lines
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        output_lines = []
        for line in process.stdout:
            if not line.strip():
                continue
            output_lines.append(line)
            log_info(line.rstrip())
        exit_code = process.wait(timeout=600)

        # Parse failing scenarios from output
        full_output = '\n'.join(output_lines)

        return {
            'worker_id': report_dir.split('_')[-1],
            'exit_code': exit_code,
            'stdout': full_output,
            'stderr': '',
            'error': None if exit_code == 0 else f"Worker {report_dir.split('_')[-1]} failed with exit code {exit_code}"
        }
    except subprocess.TimeoutExpired:
        return {
            'worker_id': report_dir.split('_')[-1],
            'exit_code': 1,
            'stdout': '',
            'stderr': 'Test timed out after 10 minutes',
            'error': 'Test timed out after 10 minutes'
        }
    except Exception as e:
        return {
            'worker_id': report_dir.split('_')[-1],
            'exit_code': 1,
            'stdout': '',
            'stderr': str(e),
            'error': str(e)
        }


def filter_features_by_tags(feature_files, tags):
    if not tags:
        return feature_files

    relevant_features = []
    for feature_file in feature_files:
        try:
            with open(feature_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Check if any of the tags are present in the feature file
                for tag in tags:
                    if tag in content:
                        relevant_features.append(feature_file)
                        break
        except Exception as e:
            log_warning(f"Could not read {feature_file}: {e}")
            # If we can't read the file, include it to be safe
            relevant_features.append(feature_file)

    return relevant_features


def run_behave_parallel(feature_files, max_workers=None, tags=None):
    # Filter feature files based on tags
    if tags:
        feature_files = filter_features_by_tags(feature_files, tags)
        log_info_emoji("📁", f"Running {len(feature_files)} relevant feature files (filtered by tags: {tags})")

    if max_workers is None:
        max_workers = min(multiprocessing.cpu_count(), len(feature_files))

    if len(feature_files) == 0:
        log_warning("⚠️  No feature files found matching the specified tags.")
        return True

    # Adjust max_workers to actual number of feature files if fewer
    actual_workers = min(max_workers, len(feature_files))
    log_info_emoji("🚀", f"Running {len(feature_files)} feature files with {actual_workers} parallel workers")
    log_info("=" * 50)

    # Create individual report directories for each worker
    report_dirs = []
    for i in range(max_workers):
        report_dir = f"reports/workers/worker_{i}"
        os.makedirs(report_dir, exist_ok=True)
        report_dirs.append(report_dir)

    # Create a pool of workers
    with multiprocessing.Pool(processes=max_workers) as pool:
        worker_tasks = distribute_features(feature_files, max_workers)

        # Run behave for each worker's feature files
        results = pool.starmap(
            run_worker_features,
            [(tasks, report_dirs[i], tags) for i, tasks in enumerate(worker_tasks) if tasks]
        )

    # Check results
    failed_tests = [result for result in results if result['exit_code'] != 0]

    # Combine Allure reports
    combine_allure_reports(report_dirs)

    log_info("=" * 50)
    if failed_tests:
        return False
    else:
        return True


def run_behave_command(args):
    """Run behave with the specified arguments and capture failing scenarios."""
    cmd = [sys.executable, '-m', 'behave']

    # Add formatter for Allure reporting
    cmd.extend(['-f', 'allure_behave.formatter:AllureFormatter', '-o', 'reports/allure-results'])

    # Add feature files if specified
    if args.features:
        cmd.extend(args.features)

    # Add tags if specified
    if args.tags:
        for tag in args.tags:
            cmd.extend(['-t', tag])

    # Run the command and capture output
    result = subprocess.run(cmd, capture_output=True, text=True)
    filtered_output = []
    for line in result.stdout.split('\n'):
        if line.strip():
            filtered_output.append(line)

    if filtered_output:
        log_info('\n'.join(filtered_output))

    return result


def main():
    args = run_options()

    os.environ['HEADLESS'] = 'True' if args.headless else 'False'
    log_info_emoji("🌐", f"Headless Mode: {str(os.environ['HEADLESS']).capitalize()}")

    os.environ['BROWSER'] = args.browser
    log_info_emoji("🌐", f"Browser: {str(args.browser).capitalize()}")

    if args.tracing:
        log_info_emoji("�� ", f"Tracing Enabled | Trace files will be saved to {TRACES_DIR}")

    create_reports_structure()

    features_dir = Path("features")
    if not features_dir.exists():
        log_failure("Error: 'features' directory not found!")
        sys.exit(1)

    # Check if feature files exist
    if not args.features:
        feature_files = list(features_dir.glob("*.feature"))
        if not feature_files:
            log_failure("Error: No feature files found in 'features' directory!")
            sys.exit(1)
        log_info_emoji("📁", f"Found {len(feature_files)} feature files")
    else:
        log_info_emoji("📁", f"Running specified feature files: {args.features}")
        feature_files = [Path(f) for f in args.features]

    # Run tests
    if args.parallel:
        log_info_emoji("🔄", "Running tests in parallel mode")
        # Determine the number of workers for parallel execution
        max_workers = args.workers if args.workers else min(multiprocessing.cpu_count(), len(feature_files))
        log_info_emoji("👥", f"Using {max_workers} workers")

        success = run_behave_parallel(feature_files, max_workers, tags=args.tags)
        result = type('Result', (), {'returncode': 0 if success else 1})()
    else:
        log_info_emoji("🔄", "Running tests in sequential mode")
        log_info("=" * 50)
        result = run_behave_command(args)

    # Handle test results
    if result.returncode == 0:
        log_success("All tests passed!")
    else:
        log_failure("Some tests failed!")

    server_report(args)
    if result.returncode != 0:
        sys.exit(result.returncode)


if __name__ == "__main__":
    main()
