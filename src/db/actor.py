from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma


async def get_all_actors() -> List[models.Actor]:
    """
    Fetch all actors from the database
    """
    try:
        async with Prisma() as db:
            return await db.actor.find_many()
    except Exception as e:
        print(f"An error occurred while fetching actors: {e}")
        return []


async def create_many_actors(
    actors: List[Dict[str, Union[str, int]]]
) -> List[models.Actor]:
    """
    Create multiple actors in the database
    """
    try:
        async with Prisma() as db:
            result = await db.actor.create_many(data=actors)
            return result
    except Exception as e:
        print(f"An error occurred while creating the actors: {e}")


async def create_one_actor(name: str, imdb_id: int) -> models.Actor:
    """
    Create an actor in the database
    """
    try:
        async with Prisma() as db:
            actor = await db.actor.create(
                data={
                    "name": name,
                    "imdbId": imdb_id,
                }
            )
            return actor
    except Exception as e:
        print(f"An error occurred while creating the actor: {e}")


async def delete_all_actors() -> None:
    """
    Delete all actors from the database and reset the auto-increment counter
    """
    print("Deleting all actors")
    try:
        async with Prisma() as db:
            await db.actor.delete_many()
            await db.execute_raw('TRUNCATE TABLE "Actor" RESTART IDENTITY')
    except Exception as e:
        print(f"An error occurred while deleting actors: {e}")
