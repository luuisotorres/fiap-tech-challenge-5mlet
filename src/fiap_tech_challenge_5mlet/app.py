from fastapi import FastAPI
from .api import api_router, auth_router

app = FastAPI(
    title="FIAP Tech Challenge 5MLET",
    version="0.1.0",
    description=(
        "FastAPI application to retrieve and serve data from "
        "Vitivinicultura Embrapa"
    )
)


app.include_router(auth_router)
app.include_router(api_router)
