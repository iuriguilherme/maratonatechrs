"""FastAPI"""

import logging
from fastapi import FastAPI

log_level: int = logging.INFO
logging.basicConfig(level = log_level)
logger: logging.Logger = logging.getLogger(__name__)

app: FastAPI = FastAPI()

@app.get("/")
async def index() -> dict:
  logger.info("hello fastapi")
  return {"message": "Deu Certo FastAPI"}

## https://github.com/TechPeloRS/maratona-pelo-rs/blob/main/docs/localizacao.md
@app.get("/localizacoes")
async def localizacoes() -> dict:
  """GET /localizacoes"""
  return {
    "localizacoes": [
      {
        "id": 1,
        "latitude": -30.0346,
        "longitude": -51.2177
      },
      {
        "id": 2,
        "latitude": -29.9128,
        "longitude": -51.1855
      }
    ]
  }

@app.post("/localizacao")
async def localizacao(latitude: float, longitude: float) -> dict:
  """POST /localizacao"""
  return {
    "id": 3,
    "latitude": -30.1234,
    "longitude": -51.1234
  }

@app.put("/localizacoes/<int:id>")
async def localizacoes(
  id: int,
  latitude: float,
  longitude: float
) -> dict:
  """PUT /localizacoes"""
  return {
    "id": 3,
    "latitude": -30.1234,
    "longitude": -51.1234
  }

@app.delete("/localizacoes/<int:id>")
async def localizacoes(id: int) -> dict:
  """DELETE /localizacoes"""
  return {
    "message": "Localização excluída com sucesso"
  }
