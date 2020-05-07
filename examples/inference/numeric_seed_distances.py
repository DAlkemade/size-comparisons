from size_comparisons.inference.baseline_numeric_gaussians import load_and_update_baseline
import logging
from datetime import datetime
from logging_setup_dla.logging import set_up_root_logger
import os

set_up_root_logger(f'SEED_{datetime.now().strftime("%d%m%Y%H%M%S")}', os.getcwd())

logger = logging.getLogger(__name__)


def main():
    # takes around 1.5 hours for the 9000 objects. So adding more objects will be pretty bad, as this will scale with n^3
    load_and_update_baseline()

if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Unhandled exception")
        raise

