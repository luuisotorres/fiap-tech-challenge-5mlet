from typing import List, Union
from pydantic import BaseModel

class ImportacaoSubproduct(BaseModel):
    product: str
    value_usd: Union[float, None] 


class ImportacaoItem(BaseModel):
    country: str
    quantity_kg: Union[float, None] 
    subproducts: List[ImportacaoSubproduct]


class ImportacaoTotal(BaseModel):
    total_overall: str

ImportacaoResponse = List[
    Union[
        ImportacaoItem,
        ImportacaoTotal
    ]
]