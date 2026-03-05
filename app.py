"""
KPI Dashboard – Application entry point.

Usage:
    python app.py          # run ETL then start the dev server
    python app.py --etl    # run ETL only (no server)
"""

import argparse
import logging
import sys

from config import FLASK_DEBUG, FLASK_HOST, FLASK_PORT
from etl import run_etl
from metrics import invalidate_cache
from web import create_app

# ── Logging setup ───────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)


def main() -> None:
    parser = argparse.ArgumentParser(description="KPI Dashboard ELT Pipeline")
    parser.add_argument(
        "--etl",
        action="store_true",
        help="Run ETL only (do not start the web server).",
    )
    args = parser.parse_args()

    # ── Step 1: ETL ─────────────────────────────────────────────────────
    logger.info("=" * 50)
    logger.info("Starting KPI Dashboard Setup …")
    logger.info("=" * 50)

    try:
        run_etl()
        invalidate_cache()
    except Exception:
        logger.exception("ETL pipeline failed – aborting.")
        sys.exit(1)

    if args.etl:
        logger.info("ETL-only mode – exiting.")
        return

    # ── Step 2: Web server ──────────────────────────────────────────────
    app = create_app()
    logger.info("Starting Flask on http://%s:%s", FLASK_HOST, FLASK_PORT)
    app.run(host=FLASK_HOST, port=FLASK_PORT, debug=FLASK_DEBUG)


if __name__ == "__main__":
    main()