from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from domain.models.main import OuterData
from domain.services.main import define_theme_category

router = APIRouter()


@router.get("/health")
def read_root():
    return {"Hello": "World"}


@router.post("/classify/")
async def process(text: OuterData):
    return JSONResponse(content=jsonable_encoder(define_theme_category(item=text)))
