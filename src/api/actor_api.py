from fastapi import APIRouter
from prisma import models
from typing import List
from db.actor import search_actor as search_actor_db

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

    # TODO: Implement search functionality
    actors = await search_actor_db(query)

    return actors
