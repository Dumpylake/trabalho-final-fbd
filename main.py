from fastapi import FastAPI # type: ignore
from crud_petshop import router as petshop_router # type: ignore

app = FastAPI(
    title="API petshop",
    version="1.0"
)

app.include_router(
    petshop_router, 
 prefix="/petshop", 
 tags=["petshop"])

app.include_router(petshop_router, prefix="/petshop", tags=["petshop"])