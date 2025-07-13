import argparse

def run_options():
    parser = argparse.ArgumentParser(
        description="Run automation tests with flexible options",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=
        """
    Examples:
      python run_tests.py                              # Run with default settings
      python run_tests.py --headless                   # Run in headless mode
      python run_tests.py --browser firefox            # Run with Firefox
      python run_tests.py --browser webkit --headless  # Run WebKit in headless mode
      python run_tests.py --parallel                   # Run tests in parallel
      python run_tests.py --parallel --headless        # Run parallel tests in headless mode
      python run_tests.py --parallel --workers 7       # Run with 7 parallel workers
      python run_tests.py --tags @smoke                # Run only smoke tests
      python run_tests.py --tags @smoke @regression    # Run smoke and regression tests
      python run_tests.py --serve-report               # Serve Allure report after tests
        """
    )

    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run tests in headless mode'
    )

    parser.add_argument(
        '--browser',
        choices=['chromium', 'firefox', 'webkit'],
        default='chromium',
        help='Browser to use for testing (default: chromium)'
    )

    parser.add_argument(
        '--parallel',
        action='store_true',
        help='Run tests in parallel using multiple workers'
    )

    parser.add_argument(
        '--workers',
        type=int,
        help='Number of parallel workers (default: CPU count or if specified)'
    )

    parser.add_argument(
        '--tags',
        nargs='+',
        help='Tags to filter tests (e.g., @smoke @regression)'
    )

    parser.add_argument(
        'features',
        nargs='*',
        help='Specific feature files to run (default: all features)'
    )

    parser.add_argument(
        '--serve-report',
        action='store_true',
        help='Serve Allure report after test completion'
    )

    return parser.parse_args()