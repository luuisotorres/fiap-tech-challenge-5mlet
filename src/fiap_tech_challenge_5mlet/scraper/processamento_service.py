from fastapi import HTTPException
from ..scraper import fetch_or_cache
from ..utils import (
    parse_processamento
)

# Mapping of available categories to their sub-option identifiers
CATEGORIES = {
    "viniferas": "subopt_01",
    "americanas_hibridas": "subopt_02",
    "uvas_de_mesa": "subopt_03",
    "sem_classificacao": "subopt_04"
}


def get_processamento_data(year: int, category: str) -> list[dict]:
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
    if category not in CATEGORIES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid category. Choose one of: viniferas"
                ", americanas_hibridas, uvas_de_mesa, sem_classificacao."
                )
        )

    suboption = CATEGORIES[category]
    url = (
        f"http://vitibrasil.cnpuv.embrapa.br/index.php"
        f"?ano={year}&opcao=opt_03&subopcao={suboption}"
    )
    cache_filename = f"processamento_{category}_{year}.html"

    try:
        html = fetch_or_cache(url, cache_filename)
    except RuntimeError:
        raise HTTPException(status_code=503,
                            detail=(
                                "Unable to access Embrapa website "
                                "or cache for processamento."))

    data = parse_processamento(html)

    if not data:
        raise HTTPException(status_code=404,
                            detail=("No processamento data found for category "
                                    f"'{category}' in year {year}."))

    return data
