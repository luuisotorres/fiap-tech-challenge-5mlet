from fastapi import HTTPException
from ..scraper import fetch_or_cache
from ..utils import parse_producao


def get_producao_data(year: int) -> list[dict]:
    """
    Retrieves and parses 'Produção' data for a given year from Embrapa,
    using a cached version when available.

    Args:
        year (int): Year to retrieve production data for.

    Returns:
        list[dict]: Parsed production data for the given year.

    Raises:
        HTTPException: If data cannot be fetched or is not available.
    """
    # Construct the URL for the Produção tab (option 02)
    url = (
        f"http://vitibrasil.cnpuv.embrapa.br/index.php"
        f"?ano={year}&opcao=opt_02"
        )
    cache_filename = f"producao_{year}.html"

    try:
        html = fetch_or_cache(url, cache_filename)
    except RuntimeError:
        raise HTTPException(status_code=503,
                            detail=(
                                "Unable to access Embrapa "
                                "or cache for produção."
                                ))

    data = parse_producao(html)

    if not data:
        raise HTTPException(status_code=404,
                            detail=f"No produção data found for year {year}.")

    return data
