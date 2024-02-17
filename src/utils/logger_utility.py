from loguru import logger
from rich.traceback import Traceback
from rich.console import Console
import io
import os
import sys
from typing import Any, Dict
from pathlib import Path


def rich_formatter(record: Dict[str, Any]) -> str:
    """Rich formatter for loguru logger"""
    format_: str = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>\n"
    )
    if record["exception"] is not None:
        output = io.StringIO()
        console = Console(file=output, force_terminal=True)
        traceback = Traceback.from_exception(*record["exception"])
        console.print(traceback)
        record["extra"]["rich_exception"] = output.getvalue()
        format_ += "{extra[rich_exception]}"
    return format_


def cleanup_old_logs(log_directory: str, max_logs: int = 10) -> None:
    """Keep only the 10 most recent log files in the directory."""
    path: Path = Path(log_directory)
    if not path.is_dir():
        return  # Not a directory or doesn't exist, nothing to clean

    # List all log files, sorted by modification time, oldest first
    logs: list[Path] = sorted(path.glob("app_*.log"), key=os.path.getmtime)

    # If there are more than max_logs, remove the oldest ones
    if len(logs) > max_logs:
        for log_file in logs[:-max_logs]:  # Keep the last max_logs files
            log_file.unlink()  # Delete the file


def setup_logger() -> None:
    """Setup the logger configuration for the application"""

    log_directory: str = "logs"
    log_file_path: str = f"{log_directory}/app_{{time}}.log"

    # Remove default logger configuration
    logger.remove()

    # Add a handler for console logging with rich formatting
    logger.add(sys.stderr, format=rich_formatter, level="INFO", colorize=True)  # type: ignore

    # Add a handler for file logging with rotation
    logger.add(log_file_path, rotation="1 week", level="DEBUG")

    # Cleanup old logs
    cleanup_old_logs(log_directory)
    """Setup the logger configuration for the application"""

    # Remove default logger configuration
    logger.remove()

    # Add a handler for console logging with rich formatting
    logger.add(sys.stderr, format=rich_formatter, level="INFO", colorize=True)  # type: ignore

    # Add a handler for file logging
    logger.add("logs/app_{time}.log", rotation="1 week", level="DEBUG")

    # Cleanup old logs
    cleanup_old_logs(log_directory)


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
