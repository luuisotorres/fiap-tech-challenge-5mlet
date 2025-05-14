from typing import List, Optional
from pydantic import BaseModel


class ExportacaoSubproduct(BaseModel):
    product: str
    value_usd: Optional[float]


class ExportacaoItem(BaseModel):
    country: str
    quantity_kg: Optional[float]
    value_usd: Optional[float]


ExportacaoResponse = List[ExportacaoItem]
