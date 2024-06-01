from fastapi import APIRouter
from prisma import models
from typing import List
from db.actor import get_all_actors

router = APIRouter()


@router.post(
    "/search/actor",
    responses={
        429: {"description": "Too Many Requests"},
    },
)
async def search_actor(q: str) -> List[models.Actor]:
    """
    Search the Boolean Model for the given query.<br>
    Example usage: http://127.0.0.1:8000/search/boolean
    """
    query = q
    print(f"Query: {query}")

    # TODO: Implement search functionality
    actors = await get_all_actors()

    return actors
