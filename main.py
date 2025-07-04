from fastapi import FastAPI

from src.api import contacts, utils
from src.middleware import ProcessTimeMiddleware

app = FastAPI()

app.add_middleware(ProcessTimeMiddleware)

app.include_router(utils.router, prefix="/api")
app.include_router(contacts.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
