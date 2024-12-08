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


async def create_many_scripts(scripts: List[Dict[str, Union[str, int]]]) -> int:
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


async def update_scripts(scripts: List[models.Script]) -> None:
    """
    Update a List of scripts in the database
    """
    list_of_ids = [script.id for script in scripts]
    list_of_scripts = []

    for script in scripts:
        list_of_scripts.append(
            {
                "id": script.id,
                "dialogue": script.dialogue,
                "movieId": script.movieId,
                "roleId": script.roleId,
                "processedDialogue": script.processedDialogue,
            }
        )

    try:
        async with Prisma() as db:
            # Split list_of_ids into chunks of 32767, because SQL cant handle more
            for i in range(0, len(list_of_ids), 32767):
                chunk_of_ids = list_of_ids[i : i + 32767]

                await db.script.delete_many(  # delete all scripts with the given ids
                    where={"id": {"in": chunk_of_ids}}
                )

                list_of_scripts_with_id = [
                    script for script in list_of_scripts if script["id"] in chunk_of_ids
                ]

                await db.script.create_many(  # reinsert the scripts
                    data=list_of_scripts_with_id,
                )
            else:
                print("No scripts to update.")

    except Exception as e:
        print(f"An error occurred while updating the scripts: {e}")


async def delete_all_scripts() -> None:
    """
    Delete all scripts from the database and reset the auto-increment counter
    """
    print("Deleting all scripts")
    try:
        async with Prisma() as db:
            # await db.script.delete_many()
            # await db.execute_raw('TRUNCATE TABLE "Script" RESTART IDENTITY')
            await db.execute_raw('TRUNCATE TABLE "Script" RESTART IDENTITY CASCADE')
    except Exception as e:
        print(f"An error occurred while deleting scripts: {e}")
