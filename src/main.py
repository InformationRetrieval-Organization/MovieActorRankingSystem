from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.actor_api import router as actor_router
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
import uvicorn
from globals import init_globals
from data_preprocessing.script_preprocessing import preprocess_scripts
from information_retrieval.vector_space_model import build_vector_space_model
from utils.classification import load_classification_model

limiter = Limiter(key_func=get_remote_address, default_limits=["30/minute"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("FastAPI app started.")

    # TODO
    init_globals()
    load_classification_model()
    await preprocess_scripts()
    await build_vector_space_model()  # is possible to execute if document frequency is implemented
    yield


app = FastAPI(
    title="Movie Actor Ranking API",
    description="API for Movie Actor Ranking.",
    version="1.0.0",
    lifespan=lifespan,
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(actor_router, tags=["Actor Search"])

# Enable CORS for the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
