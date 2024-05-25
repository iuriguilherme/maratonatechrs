"""Web"""

from jinja2 import TemplateNotFound
import logging
from quart import (
  Quart,
  render_template,
)

from . import (
  __description__ as description,
  __name__ as name,
  __version__ as version,
)

log_level: str = logging.INFO
logging.basicConfig(level = log_level)

logger: logging.Logger = logging.getLogger(__name__)

app: object = Quart(__name__)

@app.route("/")
async def index() -> str:
  try:
    markers = [
      {
        'lat': -30.0159,
        'lon': -51.1348,
        'popup': 'Porto Alegre',
      }
    ]
    return await render_template(
      "index.html",
      title = f"Protótipo: {description}",
      markers = markers,
      version = version,
    )
  except Exception as e:
    logger.exception(e)
    return await render_template(
      "error.html",
      error = repr(e),
      title = "Erro",
    )

@app.errorhandler(400)
@app.route("/error_400")
async def error_400(*e: Exception) -> str:
  """Erro genérico"""
  logger.exception(e)
  logger.warning("Erro não tratado, stacktrace acima")
  return await render_template(
    "error.html",
    error = """Tivemos um problema com esta solicitação e os \
responsáveis já foram notificados. Tente novamente mais tarde ou entre \
em contato com o suporte.""",
    title = "Não encontrado",
  ), 400

@app.errorhandler(404)
@app.errorhandler(TemplateNotFound)
@app.route("/não_existe")
async def error_404(*e: Exception) -> str:
  """Não encontrado"""
  logger.exception(e)
  logger.warning("""Tentaram acessar uma página que não existe, \
stacktrace acima""")
  return await render_template(
    "error.html",
    error = """Alguém te deu o link errado, ou esta página foi \
removida.""",
    title = "Não encontrado",
  ), 404
