from fastapi import FastAPI

from api.router import api_router
from database.session import init_db


app = FastAPI(title="Quaestor API", version="1.0.0")


@app.on_event("startup")
def on_startup() -> None:
	init_db()


@app.get("/")
def health() -> dict[str, str]:
	return {"status": "ok", "service": "quaestor-api"}


app.include_router(api_router)