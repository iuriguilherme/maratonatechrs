maratonatechrs
===

Maratona Tech pelo RS: <https://github.com/TechPeloRS/maratona-pelo-rs>  

Este projeto pretende criar um mapa interativo que agrupe informações 
de várias fontes, semelhante e inspirado nestes emergenciais criados 
pela UFRGS, mas que seja permanente e atemporal.  

A intenção é permitir que os departamentos de governo e a população 
consigam availar preventivamente qual é o risco de cada região de ser 
afetada por desastres climáticos, como por exemplo mas não limitado a 
alagamentos, deslizamentos, crise energética, abastecimento de água, 
estradas bloqueadas, etc. e subsidiar com informações potenciais 
evacuações planejadas.  

Escopo e planejamento
---

Coisas necessárias:

* Formar uma equipe
* Garimpar dados
* Decidir como manipular os dados
* Visualizar dados em um mapa
  * Criar visualização que permita escolher a data dos dados

Organizar estes pontos na ferramenta apropriada: 
https://github.com/iuriguilherme/maratonatechrs/discussions  


Desenvolvimento
---

### Tecnologia

Python; Quart; Leaflet; Open Street Maps

### Instruções

#### Windows Power Shell

```batch
$ python -m venv venv
$ .\venv\Scripts\activate
(venv) $ pip install -r requirements.txt
```

#### UNIX Bash

```bash
$ python -m venv venv
$ source venv/bin/activate
(venv) $ pip install -r requirements.txt
```

#### Pipenv

```bash
$ python -m pipenv install
```

```bash
$ pipenv run dev
```

### Lista de links usados na pesquisa

#### Geral

* https://github.com/TechPeloRS/maratona-pelo-rs
* https://www.climate.gov/maps-data/dataset/sea-level-rise-map-viewer

#### Fontes de dados

* https://prefeitura.poa.br/smpae/observapoa
* https://sos-rs.com/
* https://sites.research.google/floods/
* https://sealevel.nasa.gov/data_tools/15

#### Visualização de dados

* https://storymaps.arcgis.com/stories/02d01e5f3a2b423893a2b2560fa8ecce
* https://storymaps.arcgis.com/stories/a81d69f4bccf42989609e3fe64d8ef48
* https://disasterscharter.org/web/guest/activations/-/article/flood-in-brazil-activation-875-
* https://sealevel.nasa.gov/
* https://coast.noaa.gov/slr/
* https://sealevel.nasa.gov/task-force-scenario-tool

#### Planejamento urbano

* https://www.jiveinvestments.com/
* https://www.vincent.callebaut.org/
* https://sealevel.nasa.gov/news/206/new-high-tide-flooding-projection-tool-aids-us-coastal-decision-making


#### Tecnológico

* https://medium.com/geekculture/how-to-make-a-web-map-with-pythons-flask-and-leaflet-9318c73c67c3
* https://leafletjs.com/
* https://quart.palletsprojects.com/en/stable/index.html
* https://notabug.org/velivery/velivery_maps

Licença
---

GNU Lesser Public License v2 or any later version

Este projeto, de acordo com os termos da Maratona Tech RS, é de 
propriedade do Governo do Estado do Rio Grande do Sul.  

Leia o arquivo LICENSE incluído
