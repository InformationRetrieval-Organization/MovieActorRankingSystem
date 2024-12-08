from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma


async def get_all_actor_classifiers() -> List[models.ActorClassifier]:
    """
    Fetch all actor classifiers from the database
    """
    try:
        async with Prisma() as db:
            return await db.actorclassifier.find_many()
    except Exception as e:
        print(f"An error occurred while fetching actor classifiers: {e}")
        return []


async def create_many_actor_classifiers(
    actor_classifiers: List[Dict[str, Union[int, float]]]
) -> int:
    """
    Create multiple actor classifiers in the database
    """
    try:
        async with Prisma() as db:
            result = await db.actorclassifier.create_many(data=actor_classifiers)
            return result
    except Exception as e:
        print(f"An error occurred while creating the actor classifiers: {e}")


async def create_one_actor_classifier(
    actor_id: int,
    love_score: float,
    joy_score: float,
    anger_score: float,
    sadness_score: float,
    surprise_score: float,
    fear_score: float,
) -> models.ActorClassifier:
    """
    Create an actor classifier in the database
    """
    try:
        async with Prisma() as db:
            actor_classifier = await db.actorclassifier.create(
                data={
                    "actorId": actor_id,
                    "loveScore": love_score,
                    "joyScore": joy_score,
                    "angerScore": anger_score,
                    "sadnessScore": sadness_score,
                    "surpriseScore": surprise_score,
                    "fearScore": fear_score,
                }
            )
            return actor_classifier
    except Exception as e:
        print(f"An error occurred while creating the actor classifier: {e}")


async def delete_all_actor_classifiers() -> None:
    """
    Delete all actor classifiers from the database and reset the auto-increment counter
    """
    print("Deleting all actor classifiers")
    try:
        async with Prisma() as db:
            await db.execute_raw(
                'TRUNCATE TABLE "ActorClassifier" RESTART IDENTITY CASCADE'
            )
    except Exception as e:
        print(f"An error occurred while deleting actor classifiers: {e}")


async def search_actor_classifier(actor_id: int) -> List[models.ActorClassifier]:
    """
    Search for an actor classifier by actor id
    """
    try:
        async with Prisma() as db:
            return await db.actorclassifier.find_many(where={"actorId": actor_id})
    except Exception as e:
        print(f"An error occurred while searching for the actor classifier: {e}")
        return []


async def search_actor_classifiers(actor_ids: List[int]) -> Dict[int, int]:
    """
    Search for actor classifiers by actor ids
    """
    try:
        async with Prisma() as db:
            actor_classifiers = await db.actorclassifier.find_many(
                where={"actorId": {"in": actor_ids}}
            )
            return {
                actor_classifier.actorId: actor_classifier.id
                for actor_classifier in actor_classifiers
            }
    except Exception as e:
        print(f"An error occurred while searching for the actor classifiers: {e}")
        return {}
