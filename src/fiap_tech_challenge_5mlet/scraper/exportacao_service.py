from fastapi import HTTPException
from ..scraper import fetch_or_cache
from ..utils import (
    parse_exportacao
    )

CATEGORIES_EXPORTACAO = {
    "vinhos_de_mesa": "subopt_01",
    "espumantes": "subopt_02",
    "uvas_frescas": "subopt_03",
    "suco_de_uva": "subopt_04"
}

def get_exportacao_data(year: int, category: str) -> list[dict]:
    """
    Retrieves and parses 'Processamento' data for a given year and category
    from Embrapa, using a cached version when available.

    Args:
        year (int): Year to retrieve data for.
        category (str): One of the valid processing categories.

    Returns:
        list[dict]: Parsed processing data for the selected category and year.

    Raises:
        HTTPException: If the category is invalid or data is unavailable.
    """
    if category not in CATEGORIES_EXPORTACAO:
        raise HTTPException(
            status_code=400, 
            detail=(
                "Categoria inválida. Escolha entre: vinhos_de_mesa, espumantes, uvas_frescas, suco_de_uva."
                )
            )

    suboption = CATEGORIES_EXPORTACAO[category]
    url = (
        f"http://vitibrasil.cnpuv.embrapa.br/index.php?year={year}&suboption={suboption}&opcao=opt_06"
    )

    cache_filename = f"processamento_{category}_{year}.html"

    try:
        html = fetch_or_cache(url, cache_filename)
    except RuntimeError:
        raise HTTPException(status_code=503,
                            detail=(
                                "Unable to access Embrapa websitesite "
                                "or cache for processamento."))

    data = parse_exportacao(html)

    if not data:
        raise HTTPException(status_code=404,
                            detail=("No processamento data found for category "
                                    f"'{category}' in year {year}."))

    return data