from fastapi import HTTPException
from ..scraper import fetch_or_cache
from ..utils import (
    parse_importacao
    )

CATEGORIES_IMPORTACAO = {
    "vinhos_de_mesa": "subopt_01",
    "espumantes": "subopt_02",
    "uvas_frescas": "subopt_03",
    "uvas_passas": "subopt_04",
    "suco_de_uva": "subopt_05"
}

def get_importacao_data(year: int, category: str) -> list[dict]:
    """
    Retrieves and parses the 'Comercialização' data for a given year
    from Embrapa's website or from the local cache.

    Args:
        year (int): Year of the data to retrieve.

    Returns:
        list[dict]: A list of parsed comercialização data records.

    Raises:
        HTTPException: If the data is not found or cannot be fetched.
    """
    # Construct the URL for the given year
    if category not in CATEGORIES_IMPORTACAO:
        raise HTTPException(
            status_code=400, 
            detail=(
                "Category inválida. Escolha entre: vinhos_de_mesa, espumantes, uvas_frescas, uvas_passas, suco_de_uva."
                )
        )

    suboption = CATEGORIES_IMPORTACAO[category]
    url = (
        f"http://vitibrasil.cnpuv.embrapa.br/index.php?year={year}&suboption={suboption}&opcao=opt_05"
    )

    cache_filename = f"importacao_{category}_{year}.html"

    try:
        html = fetch_or_cache(url, cache_filename)
    except RuntimeError:
        raise HTTPException(status_code=503,
                            detail=(
                                "Unable to access Embrapa websitesite "
                                "or cache for processamento."))

    data = parse_importacao(html)

    if not data:
        raise HTTPException(status_code=404,
                            detail=("No processamento data found for category "
                                    f"'{category}' in year {year}."))

    return data