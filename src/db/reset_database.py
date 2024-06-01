import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from db.actor import create_many_actors, delete_all_actors, search_actor, search_actors
from db.movie import create_many_movies, delete_all_movies, search_movie, search_movies
from db.role import create_many_roles, delete_all_roles, search_roles
from db.script import create_many_scripts, delete_all_scripts


async def reset_database():
    await delete_all_scripts()
    await delete_all_roles()
    await delete_all_actors()
    await delete_all_movies()


if __name__ == "__main__":
    asyncio.run(reset_database())
