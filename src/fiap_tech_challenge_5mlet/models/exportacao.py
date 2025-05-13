from typing import List, Union
from pydantic import BaseModel


class ExportacaoSubproduct(BaseModel):
    product: str
    value_usd: Union[float, None] 


class ExportacaoItem(BaseModel):
    country: str
    quantity_kg: Union[float, None]
    value_usd: Union[float, None]


class ExportacaoTotal(BaseModel):
    total_overall: str


ExportacaoResponse = List[
    Union[
        ExportacaoItem,
        ExportacaoTotal
    ]
]