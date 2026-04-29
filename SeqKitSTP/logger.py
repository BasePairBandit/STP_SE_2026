# logger.py
"""
LOGGER SETUP FOR SeqKitSTP

----------------------------------------
WHAT THIS FILE DOES
----------------------------------------
This file creates and configures a logger for the entire project.

It:
✔ Creates a logger called "SeqKitSTP"
✔ Sends log messages to the terminal (console)
✔ Saves log messages to a file in: project_root/logs/seqkitstp.log
✔ Ensures logs are formatted consistently


----------------------------------------
HOW TO USE THIS LOGGER
----------------------------------------
In other files, simply import and use it:

    from SeqKitSTP.logger import logger

    logger.debug("Detailed debugging info")
    logger.info("Normal message")
    logger.warning("Something might be wrong")
    logger.error("Something failed")


----------------------------------------
LOGGING LEVELS (WHEN TO USE EACH)
----------------------------------------
DEBUG    → Detailed technical information (for developers)
INFO     → Normal program operation messages
WARNING  → Something unexpected, but program continues
ERROR    → Something failed during execution
CRITICAL → Serious failure, program may stop


----------------------------------------
IMPORTANT NOTES
----------------------------------------
✔ Logging is configured ONLY ONCE in this file
✔ Other files should NOT reconfigure logging
✔ Import the logger and use it — do not recreate it

✔ Console shows: INFO and above
✔ Log file stores: DEBUG and above (everything)

✔ A safety check prevents duplicate log messages if this file
  is imported multiple times


----------------------------------------
MENTAL MODEL
----------------------------------------
Your code → logger → handlers → outputs

logger   = central logging tool
handlers = where logs go (console, file)
outputs  = terminal + log file
"""

import logging
import os


# Create (or retrieve) the logger
logger = logging.getLogger("SeqKitSTP")
logger.setLevel(logging.DEBUG)


# Prevent duplicate handlers if imported multiple times
if not logger.handlers:

    # Find project root (1 level up from this file)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, ".."))

    # Create logs directory
    logs_dir = os.path.join(project_root, "logs")
    os.makedirs(logs_dir, exist_ok=True)

    # Log file path
    log_file = os.path.join(logs_dir, "seqkitstp.log")

    # Log message format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(filename)s:%(lineno)d | %(message)s"
    )

    # Console handler (prints to terminal)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # File handler (writes to file)
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # Attach handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
