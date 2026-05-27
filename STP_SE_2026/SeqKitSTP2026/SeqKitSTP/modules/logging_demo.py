# logging_demo.py
"""
LOGGING DEMONSTRATION SCRIPT

----------------------------------------
WHAT THIS SCRIPT DOES
----------------------------------------
This script demonstrates how to use logging properly
by retrieving a logger and using different log levels.

----------------------------------------
IMPORTANT CONCEPT
----------------------------------------
Logging is configured centrally (in logger.py).

Here, we DO NOT import a logger object.
Instead, we retrieve it using:

    logging.getLogger("SeqKitSTP")

This ensures:
✔ All files use the same logger
✔ Logging remains consistent across the project

----------------------------------------
LOGGING LEVELS DEMONSTRATED
----------------------------------------
DEBUG    → Detailed technical information (for developers)
INFO     → Normal program operation messages
WARNING  → Something unexpected, but program continues
ERROR    → Something failed during execution
CRITICAL → Serious failure, program may stop
"""

# Step 1: Import the logging setup (this runs configuration once)
from SeqKitSTP import logger  # ensures logging is configured

# Step 2: Get the logger (this is the key idea)
import logging
logger = logging.getLogger("SeqKitSTP")


# --------------------------------------------------
# DEMO: Different logging levels
# --------------------------------------------------

logger.debug("DEBUG: Detailed info for debugging problems.")

logger.info("INFO: The program has started successfully.")

logger.warning("WARNING: Something unexpected happened, but continuing.")

logger.error("ERROR: Something failed during execution.")

logger.critical("CRITICAL: Serious failure - program may stop.")


# --------------------------------------------------
# FINAL MESSAGE
# --------------------------------------------------

logger.info("Demo complete. Check the console and log file.")

