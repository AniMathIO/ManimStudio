from loguru import logger
from rich.traceback import Traceback
from rich.console import Console
import io
import sys


def rich_formatter(record):
    """Rich formatter for loguru logger"""
    format_ = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n"
    if record["exception"] is not None:
        output = io.StringIO()
        console = Console(file=output, force_terminal=True)
        traceback = Traceback.from_exception(*record["exception"])
        console.print(traceback)
        record["extra"]["rich_exception"] = output.getvalue()
        format_ += "{extra[rich_exception]}"
    return format_


def setup_logger():
    """Setup the logger configuration for the application"""

    # Remove default logger configuration
    logger.remove()

    # Add a handler for console logging with rich formatting
    logger.add(sys.stderr, format=rich_formatter, level="INFO", colorize=True)

    # Add a handler for file logging
    logger.add("logs/app_{time}.log", rotation="1 week", level="DEBUG")


setup_logger()

# Example log messages:
# @logger.catch
# def divide(a, b):
#     a / b


# divide(1, 0)

# logger.info("This is an info message")
# logger.debug("This is a debug message")
# logger.warning("This is a warning message")
# logger.error("This is an error message")
# logger.critical("This is a critical message")
