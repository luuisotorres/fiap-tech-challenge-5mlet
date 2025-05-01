from typing import List, Union
from pydantic import BaseModel


class ProducaoSubproduct(BaseModel):
    product: str
    quantity_liters: str


class ProducaoItem(BaseModel):
    product: str
    quantity_liters: str
    subproducts: List[ProducaoSubproduct]


class ProducaoTotal(BaseModel):
    total_overall: str


# Full response from the /producao endpoint
ProducaoResponse = List[
    Union[
        ProducaoItem,
        ProducaoTotal
    ]
]
