# logger.py
import logging
from datetime import datetime

log_file = f"utils/log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,  # Default level
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger()