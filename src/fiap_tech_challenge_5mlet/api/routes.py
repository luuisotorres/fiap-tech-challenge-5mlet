from fastapi import APIRouter, Depends
from fastapi.responses import HTMLResponse
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


@router.get("/", 
            response_class=HTMLResponse,
            tags=["Root"])
def read_root():
        return """
     <html>
        <head>
            <title>🍇 FIAP Tech Challenge 5MLET</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    background-color: #f4f4f9;
                    color: #333;
                }
                h1 {
                    font-size: 6rem;
                    color: #4A148C;
                }
                p {
                    font-size: 2.5rem;
                    margin-top: 12px;
                }
                a {
                    text-decoration: none;
                    color: #2196F3;
                    font-weight: bold;
                }
            </style>
        </head>
        <body>
            <h1>🍇 FIAP Tech Challenge 5MLET API</h1>
            <p><b>Welcome to the Embrapa Vitivinicultura data API 🎉</b></p>
            <p>🔐 Authenticated endpoints available at <a href='/docs'>/docs</a></p>
        </body>
    </html>
    """


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
