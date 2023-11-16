from fastapi import Depends, HTTPException, APIRouter
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from domain.models.url import OuterData
from domain.services.scraper import parse_all_urls, gateway

router = APIRouter()


@router.get("/health")
def read_root():
    return {"Hello": "World"}


@router.post("/process_urls/")
async def process(list_urls: OuterData):
    # todo: middleware to check url; logg data
    data = await gateway(urls=list_urls.urls)
    for url in list_urls:
        print(url)
    return JSONResponse(content=jsonable_encoder(data))
