from fastapi import HTTPException
from ..scraper import fetch_or_cache
from ..utils import (
    parse_comercializacao
    )


def get_comercializacao_data(year: int) -> list[dict]:
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
    url = (
        "http://vitibrasil.cnpuv.embrapa.br/index.php"
        f"?ano={year}&opcao=opt_04"
    )

    # Define the cache filename based on the year
    cache_filename = f"comercializacao_{year}.html"

    try:
        # Attempt to fetch the HTML or load it from cache
        html = fetch_or_cache(url, cache_filename)
    except RuntimeError:
        raise HTTPException(status_code=503,
                            detail="Unable to access Embrapa or cache.")

    # Parse the HTML to extract structured data
    data = parse_comercializacao(html)

    if not data:
        raise HTTPException(status_code=404,
                            detail=f"No data found for year {year}.")

    return data
