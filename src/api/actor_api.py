from fastapi import APIRouter

router = APIRouter()

@router.post(
    "/search/actor",
    responses={
        429: {"description": "Too Many Requests"},
    },
)
async def search_actor(q: str) -> None:
    """
    Search the Boolean Model for the given query.<br>
    Example usage: http://127.0.0.1:8000/search/boolean
    """
    query = q

    return None