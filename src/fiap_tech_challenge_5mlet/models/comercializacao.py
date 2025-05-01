from typing import List, Union
from pydantic import BaseModel


class Subproduct(BaseModel):
    product: str
    quantity_liters: str


class ComercializacaoItem(BaseModel):
    product: str
    quantity_liters: str
    subproducts: List[Subproduct]


class ComercializacaoTotal(BaseModel):
    total_overall: str


# Response returned by the endpoint
ComercializacaoResponse = List[
    Union[
        ComercializacaoItem,
        ComercializacaoTotal
    ]
]
