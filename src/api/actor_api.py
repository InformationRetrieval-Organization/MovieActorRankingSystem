from fastapi import APIRouter
from prisma import models
from typing import List
from db.actor import search_actor as search_actor_db
from information_retrieval.token_vector_space_model import (
    search_token_vector_space_model,
)
from information_retrieval.classified_vector_space_model import (
    search_classified_vector_space_model,
)

router = APIRouter()


@router.get(
    "/search/actor",
    responses={
        429: {"description": "Too Many Requests"},
    },
)
async def search_actor(q: str) -> List[models.Actor]:
    """
    Search for actors by name.<br>
    Example usage: http://127.0.0.1:8000/search/actor
    """
    query = q
    print(f"Query: {query}")

    # search classified vector space model
    actors = await search_classified_vector_space_model(query)

    print(f"returning {len(actors)} actors")

    return actors


@router.get(
    "/search/token_vectorspace/actor",
    responses={
        429: {"description": "Too Many Requests"},
    },
)
async def search_token_vectorspace_actor(q: str) -> List[models.Actor]:
    """
    Search for actors by token vector space
    """
    query = q
    print(f"Query: {query}")

    # search matching actors with vector space model
    actors = await search_token_vector_space_model(query)

    print(f"returning {len(actors)} actors")

    return actors
