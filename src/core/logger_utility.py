from loguru import logger
from rich.logging import RichHandler
import sys


# Configure Loguru logger
def setup_logger():
    # Remove default logger configuration
    logger.remove()

    # Add a handler for console logging with rich formatting
    logger.add(
        sys.stderr, format="{time} {level} {message}", level="INFO", colorize=True
    )
    logger.configure(
        handlers=[
            {
                "sink": RichHandler(markup=True),
                "format": " <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
            }
        ]
    )

    # Add a handler for file logging
    logger.add("logs/app_{time}.log", rotation="1 week", level="DEBUG")


setup_logger()

# Example logging
logger.info("This is an informational message.")
logger.debug("This is a debug message.")
logger.error("This is an error message.")
logger.warning("This is a warning message.")
