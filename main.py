from fastapi import FastAPI # type: ignore
from crud_petshop import router as petshop_router # type: ignore
from crud_cliente import router as cliente_router
from crud_animal import router as animal_router

app = FastAPI(
    title="API petshop",
    version="1.0"
)

app.include_router(petshop_router, prefix="/petshop", tags=["petshop"])
app.include_router(cliente_router, prefix="/cliente", tags=["cliente"])
app.include_router(animal_router, prefix="/animal", tags=["animal"])