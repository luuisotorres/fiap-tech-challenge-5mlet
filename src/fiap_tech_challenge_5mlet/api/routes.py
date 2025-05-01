from fastapi import APIRouter, Depends
from typing import Literal
from ..scraper import (
    get_comercializacao_data,
    get_processamento_data,
    get_producao_data
)
from ..models import (
    ComercializacaoResponse,
    ProducaoResponse,
    ProcessamentoResponse
)
from ..auth import (
    require_token
)

router = APIRouter()


@router.get("/", tags=["Root"])
def read_root():
    return {"message": "API is working!"}


# Create Endpoint: GET /comercializacao
@router.get("/comercializacao",
            response_model=ComercializacaoResponse,
            tags=["Comercialização"],
            dependencies=[Depends(require_token)])
def comercializacao(year: int = 2023) -> ComercializacaoResponse:
    """
    Endpoint to retrieve parsed 'Comercialização' data from Embrapa for a
    given year.

    Args:
        year (int): The year for which to fetch and return data
        for comercialização.

    Returns:
        list[dict]: A list of structured comercialização data including
        products and subproducts.
    """
    return get_comercializacao_data(year)


# Creat Endpoint: GET /processamento
@router.get("/processamento",
            response_model=ProcessamentoResponse,
            tags=["Processamento"],
            dependencies=[Depends(require_token)])
def processamento(
    year: int = 2023,
    category: Literal[
        "viniferas",
        "americanas_hibridas",
        "uvas_de_mesa",
        "sem_classificacao"
    ] = "viniferas",
) -> ProcessamentoResponse:
    """
    Endpoint to retrieve parsed 'Processamento' data from Embrapa
    for a given year and category.

    Args:
        year (int): The year of data to retrieve.
        category (str): The category to filter by (viniferas,
                                                   americanas_hibridas,
                                                   uvas_de_mesa,
                                                   sem_classificacao)

    Returns:
        list[dict]: Structured processamento data for the specified year
        category
    """
    return get_processamento_data(year, category)


# Create Endpoint: GET /producao
@router.get("/producao",
            response_model=ProducaoResponse,
            tags=["Produção"],
            dependencies=[Depends(require_token)])
def producao(year: int = 2023) -> ProducaoResponse:
    """
    Endpoint to retrieve parsed 'Produção' data from Embrapa
    for a given year.

    Args:
        year (int): The year of data to retrieve

    Returns:
        list[dict]: Structured produção data for the
        specified year.
    """
    return get_producao_data(year)
