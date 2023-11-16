from fastapi import FastAPI
import uvicorn

from app.finder import search_links
from app.logger import logger
from app.schema import UserInput

app = FastAPI()


@app.get("/")
def read_root():
    logger.info(f"called")
    return {"Hello": "world"}


@app.post("/find_related/")
async def process_text(data: UserInput):
    # Получите текст из запроса
    text = data.url
    logger.info(f"get data: {text}")

    answer = await search_links(source_request=data)

    return answer.to_dict()


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8012)
