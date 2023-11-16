import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from adapter.api.classificator import router as user_router
from inject import settings, get_cors_address

app = FastAPI()
app.include_router(user_router)

origins = get_cors_address()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=settings.app_port)
