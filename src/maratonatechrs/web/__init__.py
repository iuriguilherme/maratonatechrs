"""Web"""

from jinja2 import TemplateNotFound
import logging
logger: logging.Logger = logging.getLogger(__name__)

try:
    import os
    from quart import (
        Quart,
        render_template,
        request,
    )
    from quart_wtf.csrf import CSRFProtect
    import secrets
    from werkzeug.utils import secure_filename
    from .. import (
        __description__ as description,
        __name__ as name,
        __version__ as version,
    )
    from .forms import (
      MarkerForm,
      PolygonForm,
    )
except Exception as e:
    logger.exception(e)
    raise

app: object = Quart(__name__)
app.secret_key: str = os.getenv('QUART_SECRET',
    default = secrets.token_urlsafe(32))

## Porto Alegre LatLng(-30.028344, -51.228529)
markers: list[dict[str, str | float]] = [
    {
        'lat': -30.028344,
        'lon': -51.228529,
        'popup': 'Porto Alegre',
    }
]

@app.route("/")
async def index() -> str:
    try:
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

@app.route("/marcador", methods = ['GET', 'POST'])
async def marcador() -> str:
    """Cadastrar novo marcador"""
    try:
        cadastrado: bool = False
        logger.info(f"request.form: {await request.form}")
        logger.info(f"form fields: {[f for f in (await request.form)]}")
        logger.info("form-zero" in (await request.form))
        form: MarkerForm = MarkerForm(formdata = await request.form)
        if request.method == "POST":
            logger.info(f"Formulário: {form} ({type(form)})")
            try:
                markers.append({
                    'lat': form["latitude_field"].data,
                    'lon': form["longitude_field"].data,
                    'popup': form["description_field"].data
                })
                cadastrado = True
            except:
                raise
        return await render_template(
            "marcador.html",
            form = form,
            title = "Cadastrar marcador",
            cadastrado = cadastrado,
        )
    except Exception as e:
        logger.exception(e)
        return await render_template(
            "error.html",
            error = repr(e),
            title = "Erro",
        )

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    form: PolygonForm = PolygonForm()
    if form.validate_on_submit():
        f = form.photo.data
        filename = secure_filename(f.filename)
        f.save(os.path.join(
            app.instance_path, 'photos', filename
        ))
        return redirect(url_for('index'))

    return render_template('upload.html', form=form)

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
