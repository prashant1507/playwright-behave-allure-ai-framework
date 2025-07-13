import logging
import sys
from datetime import datetime


class CustomFormatter(logging.Formatter):
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    RESET = '\033[0m'

    def format(self, record):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = record.getMessage()
        log_line = f"{timestamp} | {message}"
        
        # Color based on log level
        if record.levelno >= logging.ERROR:
            log_line = f"{self.RED}{log_line}{self.RESET}"
        elif record.levelno == logging.WARNING:
            log_line = f"{self.YELLOW}{log_line}{self.RESET}"
        elif "✅" in message or "success" in message.lower():
            log_line = f"{self.GREEN}{log_line}{self.RESET}"
        elif "❌" in message or "failing" in message.lower():
            log_line = f"{self.RED}{log_line}{self.RESET}"
        elif "⚠️" in message or "warning" in message.lower():
            log_line = f"{self.YELLOW}{log_line}{self.RESET}"
        elif "📊" in message or "📁" in message or "🚀" in message or "👥" in message or "🔄" in message:
            log_line = f"{self.CYAN}{log_line}{self.RESET}"
        elif "🌐" in message:
            log_line = f"{self.BLUE}{log_line}{self.RESET}"
        else:
            log_line = f"{self.MAGENTA}{log_line}{self.RESET}"
        
        return log_line


def setup_logger(name="test_framework", level=logging.INFO):
    """Setup and return a custom logger with the specified format."""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Clear any existing handlers to avoid duplicates
    logger.handlers.clear()
    
    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    
    # Create formatter and add it to the handler
    formatter = CustomFormatter()
    console_handler.setFormatter(formatter)
    
    # Add filter to suppress PyCharm debugging errors
    class PyCharmFilter(logging.Filter):
        def filter(self, record):
            message = record.getMessage()
            # Filter out PyCharm debugging errors and threading issues
            if any(keyword in message for keyword in [
                "pydevd", "Exception ignored", "Traceback", 
                "TypeError: 'NoneType' object is not subscriptable",
                "threading.py", "current_thread", "Using selector"
            ]):
                return False
            return True
    
    console_handler.addFilter(PyCharmFilter())
    
    # Add the handler to the logger
    logger.addHandler(console_handler)
    
    return logger


# Create a default logger instance
default_logger = setup_logger()


def log_info(message):
    default_logger.info(message)


def log_error(message):
    default_logger.error(message)


def log_warning(message):
    default_logger.warning(message)


def log_debug(message):
    default_logger.debug(message)


def log_success(message):
    default_logger.info(f"✅ {message}")


def log_failure(message):
    default_logger.error(f"❌ {message}")


def log_info_emoji(emoji, message):
    default_logger.info(f"{emoji} {message}")


def log_error_emoji(emoji, message):
    default_logger.error(f"{emoji} {message}") 