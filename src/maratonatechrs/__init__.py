"""maratonatechrs"""

import logging
import os

log_level: str = os.getenv('LOG_LEVEL', default = logging.INFO)
logging.basicConfig(level = log_level)
logger: logging.Logger = logging.getLogger(__name__)

from ._version import __version__

__name__: str = "maratonatechrs"
__description__: str = "Projeto para Maratona Tech RS"

print(f"{__name__}: {__description__}")
