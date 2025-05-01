from typing import List, Union
from pydantic import BaseModel


class ProcessamentoSubproduct(BaseModel):
    product: str
    quantity_kg: str


class ProcessamentoItem(BaseModel):
    product: str
    quantity_kg: str
    subproducts: List[ProcessamentoSubproduct]


class ProcessamentoTotal(BaseModel):
    total_overall: str


# Response from /processamento endpoint — a list of products and a total block
ProcessamentoResponse = List[
    Union[
        ProcessamentoItem,
        ProcessamentoTotal
    ]
]
