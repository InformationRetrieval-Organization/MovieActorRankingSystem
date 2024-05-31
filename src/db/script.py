from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma


async def get_all_scripts() -> List[models.Script]:
    """
    Fetch all scripts from the database
    """
    try:
        async with Prisma() as db:
            return await db.script.find_many()
    except Exception as e:
        print(f"An error occurred while fetching scripts: {e}")
        return []


async def create_many_scripts(
    scripts: List[Dict[str, Union[str, int]]]
) -> List[models.Script]:
    """
    Create multiple scripts in the database
    """
    try:
        async with Prisma() as db:
            result = await db.script.create_many(data=scripts)
            return result
    except Exception as e:
        print(f"An error occurred while creating the scripts: {e}")


async def create_one_script(
    dialogue: str, movie_id: int, role_id: int
) -> models.Script:
    """
    Create a script in the database
    """
    try:
        async with Prisma() as db:
            script = await db.script.create(
                data={
                    "dialogue": dialogue,
                    "movieId": movie_id,
                    "roleId": role_id,
                }
            )
            return script
    except Exception as e:
        print(f"An error occurred while creating the script: {e}")


async def delete_all_scripts() -> None:
    """
    Delete all scripts from the database and reset the auto-increment counter
    """
    print("Deleting all scripts")
    try:
        async with Prisma() as db:
            await db.script.delete_many()
            await db.execute_raw('TRUNCATE TABLE "Script" RESTART IDENTITY')
    except Exception as e:
        print(f"An error occurred while deleting scripts: {e}")
