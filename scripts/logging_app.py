# logging is focusly intended for getting an information based on the level of the system warn.
import logging

logging.basicConfig(
    filename="outputs/logs/system.log",
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
)

logger = logging.getLogger(__name__)

# dd