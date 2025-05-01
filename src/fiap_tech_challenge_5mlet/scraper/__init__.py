from .html_fetcher import fetch_or_cache
from .comercializacao_service import get_comercializacao_data
from .processamento_service import get_processamento_data
from .producao_service import get_producao_data

__all__ = [
    "fetch_or_cache",
    "get_comercializacao_data",
    "get_processamento_data",
    "get_producao_data"
    ]
