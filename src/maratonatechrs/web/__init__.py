"""Web"""

import logging
logger: logging.Logger = logging.getLogger(__name__)

try:
    import aiohttp
    from jinja2 import TemplateNotFound
    import json
    import os
    import pathlib
    from pykml import parser
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
      Update1Form,
      Update2Form,
      Update3Form,
    )
except Exception as e:
    logger.exception(e)
    raise

app: object = Quart(__name__)
app.secret_key: str = os.getenv(
    'QUART_SECRET',
    default = secrets.token_urlsafe(32)
)
csrf: object = CSRFProtect(app)

## Porto Alegre LatLng(-30.028344, -51.228529)
markers: list[dict[str, str | float]] = [
    {
        'lat': -30.028344,
        'lon': -51.228529,
        'popup': 'Porto Alegre',
    }
]
polygons: list[dict] = [
    {
        'latlongs': [
            [-30.033273, -51.240696],
            [-30.030775, -51.238883],
            [-30.019627, -51.216674],
            [-30.017825, -51.197619],
            [-30.022322, -51.195409],
            [-30.028583, -51.19454],
            [-30.040406, -51.194444],
            [-30.048343, -51.196375],
            [-30.052692, -51.204722],
            [-30.060842, -51.219635],
            [-30.059378, -51.230729],
            [-30.04226, -51.236136],
            [-30.041388, -51.241157],
            [-30.041388, -51.241157]
        ],
        'color': 'orange',
        'description': "Polígono de teste",
    }
]
mapa_cores: dict = {
    1: "red",
    2: "orange",
    3: "yellow",
    4: "green",
}

@app.route("/")
async def index() -> str:
    try:
        return await render_template(
            "index.html",
            title = f"Protótipo: {description}",
            markers = markers,
            polygons = polygons,
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

@app.route("/poligono", methods = ['GET', 'POST'])
async def poligono() -> str:
    """Cadastrar novo polígono"""
    try:
        cadastrado: bool = False
        form: PolygonForm = await PolygonForm().create_form()
        if await form.validate_on_submit():
            try:
                arquivo: object = form["kml_field"].data
                caminho: str = os.path.join(
                    app.instance_path,
                    'kml',
                    secure_filename(arquivo.filename)
                )
                pathlib.Path(os.path.dirname(caminho)).mkdir(
                    parents = True, exist_ok = True)
                await arquivo.save(caminho)
                kml: object | None = None
                with open(caminho) as a:
                    kml = parser.parse(a)
                ## Troféu de ouro código feio do ano
                coordenadas: list = [
                    [float(j[1]), float(j[0])] for j in \
                    [i.strip().split(',') for i in \
                    kml.getroot().Document.Placemark.Polygon.
                    outerBoundaryIs.LinearRing.coordinates.text.
                    split('\n')[1:-1]]
                ]
                polygons.append({
                    'latlongs': coordenadas,
                    'color': 'green',
                    'description': "DEU CERTO",
                })
                cadastrado = True
            except Exception as e:
                logger.exception(e)
        return await render_template(
            "poligono.html",
            form = form,
            title = "Cadastrar polígono",
            cadastrado = cadastrado,
        )
    except Exception as e:
        logger.exception(e)
        return await render_template(
            "error.html",
            error = repr(e),
            title = "Erro",
        )

@app.route("/dados/enchente", methods = ['GET', 'POST'])
async def dados_enchente() -> str:
    """Enchentes UK"""
    try:
        api_enchentes_url: str = """http://environment.data.gov.uk/floo\
d-monitoring/id/floods"""
        arquivo_enchentes: str = os.path.join(
            app.instance_path,
            'uk',
            'flood.json',
        )
        pathlib.Path(os.path.dirname(arquivo_enchentes)).mkdir(
            parents = True, exist_ok = True)
        caminho_enchentes: str = os.path.join(
            os.path.dirname(arquivo_enchentes),
            'floods',
        )
        pathlib.Path(caminho_enchentes).mkdir(
            parents = True, exist_ok = True)
        atualizado1: bool = False
        atualizado2: bool = False
        atualizado3: bool = False
        form1: Update1Form = await Update1Form().create_form()
        form2: Update2Form = await Update2Form().create_form()
        form3: Update3Form = await Update3Form().create_form()
        if form1.submit1_field.data and await form1.validate():
            try:
                async with aiohttp.ClientSession() as s:
                    async with s.get(api_enchentes_url) as r:
                        if r.status:
                            with open(arquivo_enchentes, 'w+') as f:
                                json.dump(await r.json(), f)
                            atualizado1 = True
            except:
                raise
        elif form2.submit2_field.data and await form2.validate():
            try:
                with open(arquivo_enchentes, 'r+') as f:
                    dados_enchentes: dict = json.load(f)
                for item in dados_enchentes['items']:
                    enchente: str = os.path.join(
                        caminho_enchentes,
                        item['floodAreaID'],
                    )
                    if not os.path.isfile(os.path.join(enchente,
                        'polygon.json')
                    ):
                        pathlib.Path(enchente).mkdir(
                            parents = True, exist_ok = True)
                        with open(os.path.join(enchente,
                            'metadata.json'), 'w+'
                        ) as f:
                            json.dump({
                                'description': item.get('message',
                                    item.get('description')),
                                'color': mapa_cores[
                                    item['severityLevel']],
                            }, f)
                        async with aiohttp.ClientSession() as s:
                            async with \
                                s.get(item['floodArea']['polygon']) as \
                            r:
                                if r.status:
                                    with open(os.path.join(enchente,
                                        'polygon.json'), 'w+'
                                    ) as f:
                                        json.dump(await r.json(), f)
                atualizado2 = True
            except:
                raise
        elif form3.submit3_field.data and await form3.validate():
            try:
                for enchente in os.listdir(caminho_enchentes):
                    if os.path.isdir(os.path.join(caminho_enchentes,
                        enchente)
                    ):
                        dados: dict = {}
                        with open(os.path.join(caminho_enchentes,
                            enchente, 'metadata.json'), 'r+'
                        ) as f:
                            dados = json.load(f)
                        with open(os.path.join(caminho_enchentes,
                            enchente, 'polygon.json'), 'r+'
                        ) as f:
                            _poligonos = json.load(f)
                            description: str = _poligonos['features']\
                                [0]['properties']['DESCRIP']
                            for _c1 in _poligonos['features'][0]\
                                ['geometry']['coordinates']\
                            :
                                for _c2 in _c1:
                                    latlongs: list = []
                                    for _c3 in _c2:
                                        if isinstance(_c3, list):
                                            latlongs.append([_c3[1],
                                                _c3[0]])
                                        else:
                                            logger.info(f"""{enchente} \
inconsistente""")
                                    polygons.append({
                                        'color': dados['color'],
                                        'description': description,
                                        'latlongs': latlongs,
                                    })
                atualizado3 = True
            except:
                raise
        return await render_template(
            "dados/enchente.html",
            title = "Enchentes Inglaterra",
            form1 = form1,
            form2 = form2,
            form3 = form3,
            atualizado1 = atualizado1,
            atualizado2 = atualizado2,
            atualizado3 = atualizado3,
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
