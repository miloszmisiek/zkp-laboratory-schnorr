from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.routers import params, v1
from app.state import ServerState


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.server_state = ServerState()
    yield


app = FastAPI(title="Lab Server - ZKP", lifespan=lifespan)


@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


app.include_router(params.router)
app.include_router(v1.router)
