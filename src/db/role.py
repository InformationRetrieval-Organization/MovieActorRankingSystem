from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma


async def get_all_roles() -> List[models.Role]:
    """
    Fetch all roles from the database
    """
    try:
        async with Prisma() as db:
            return await db.role.find_many()
    except Exception as e:
        print(f"An error occurred while fetching roles: {e}")
        return []


async def create_many_roles(roles: List[Dict[str, Union[str, int]]]) -> int:
    """
    Create multiple roles in the database
    """
    try:
        async with Prisma() as db:
            result = await db.role.create_many(data=roles)
            return result
    except Exception as e:
        print(f"An error occurred while creating the roles: {e}")


async def create_one_role(name: str, movie_id: int, actor_id: int) -> models.Role:
    """
    Create a role in the database
    """
    try:
        async with Prisma() as db:
            role = await db.role.create(
                data={
                    "name": name,
                    "movieId": movie_id,
                    "actorId": actor_id,
                }
            )
            return role
    except Exception as e:
        print(f"An error occurred while creating the role: {e}")


async def delete_all_roles() -> None:
    """
    Delete all roles from the database and reset the auto-increment counter
    """
    print("Deleting all roles")
    try:
        async with Prisma() as db:
            # await db.role.delete_many()
            # await db.execute_raw('TRUNCATE TABLE "Role" RESTART IDENTITY')
            await db.execute_raw('TRUNCATE TABLE "Role" CASCADE')
    except Exception as e:
        print(f"An error occurred while deleting roles: {e}")


async def search_role(title: str) -> List[models.Role]:
    """
    Search for a role by title
    """
    try:
        async with Prisma() as db:
            return await db.role.find_many(where={"name": {"contains": title}})
    except Exception as e:
        print(f"An error occurred while searching for a role: {e}")
        return []


async def search_roles(titles: List[str]) -> Dict[str, int]:
    """
    Search for roles by titles
    """
    try:
        async with Prisma() as db:
            roles = await db.role.find_many(where={"name": {"in": titles}})
            return {role.name: role.id for role in roles}
    except Exception as e:
        print(f"An error occurred while searching for roles: {e}")
        return {}
