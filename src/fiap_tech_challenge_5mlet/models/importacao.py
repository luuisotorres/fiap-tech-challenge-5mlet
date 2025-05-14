from typing import List, Optional
from pydantic import BaseModel


class ImportacaoItem(BaseModel):
    country: str
    quantity_kg: Optional[float]
    value_usd: Optional[float]


ImportacaoResponse = List[ImportacaoItem]
