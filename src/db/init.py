import pandas as pd
import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from db.actor import create_many_actors, delete_all_actors
from db.movie import create_many_movies, delete_all_movies
from db.role import create_many_roles, delete_all_roles
from db.script import create_many_scripts, delete_all_scripts
from config import (
    PRO_IMDB_MOV_ROL_FILE_PATH,
    PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH,
)


async def init_database():
    """
    Initialize the database by deleting the existing posts and processed_posts and inserting the articles from the files into the database
    """

    await delete_all_actors()
    await delete_all_movies()
    await delete_all_roles()
    await delete_all_scripts()

    await insert_actors()
    await insert_movies()
    await insert_roles()
    await insert_scripts()


async def insert_actors():
    """
    Insert all actors into the database
    """
    df = pd.read_csv(PRO_IMDB_MOV_ROL_FILE_PATH)

    actors = df[["actor", "imdb_actor_id"]].drop_duplicates()
    actors.columns = ["name", "imdbId"]  # Rename columns
    actors = actors.to_dict("records")

    await create_many_actors(actors)


async def insert_movies():
    """
    Insert all movies into the database
    """
    df = pd.read_csv(PRO_IMDB_MOV_ROL_FILE_PATH)

    movies = df[["title", "imdb_movie_id"]].drop_duplicates()
    movies.columns = ["title", "imdbId"]  # Rename columns
    movies = movies.to_dict("records")

    await create_many_movies(movies)


async def insert_roles(df: pd.DataFrame):
    """
    Insert all roles into the database
    """
    df = pd.read_csv(PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH)

    roles = df[["role", "imdb_role_id"]].drop_duplicates()
    roles.columns = ["name", "imdbId"]  # Rename columns
    roles = roles.to_dict("records")

    await create_many_roles(roles)


async def insert_scripts(df: pd.DataFrame):
    """
    Insert all scripts into the database
    """
    df = pd.read_csv(PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH)

    scripts = df[["dialogueText", "imdb_role_id", "imdb_movie_id"]].drop_duplicates()
    scripts.columns = ["dialogue", "roleId", "movieId"]  # Rename columns
    scripts = scripts.to_dict("records")

    await create_many_scripts(scripts)


if __name__ == "__main__":
    asyncio.run(init_database())
