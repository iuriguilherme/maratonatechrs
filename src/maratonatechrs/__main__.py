"""maratonatechrs"""

import logging
import uvicorn

from . import __description__, __version__, web

log_level: int = logging.INFO
logging.basicConfig(level = log_level)

logger: logging.Logger = logging.getLogger(__name__)

logger.info(f"{__description__} {__version__} carregado como módulo")

try:
  uvicorn.run(
    web.app,
    # ~ uds = 'app.socket',
    host = '127.0.0.1',
    port = 8000,
    # ~ forwarded_allow_ips = True,
    # ~ proxy_headers = True,
    # ~ timeout_keep_alive = 1,
    log_level = log_level,
    # ~ reload = True,
  )
except Exception as e:
  logger.exception(e)

logger.info("Tchau")
