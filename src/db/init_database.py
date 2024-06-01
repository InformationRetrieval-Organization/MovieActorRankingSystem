import pandas as pd
import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from db.actor import create_many_actors, delete_all_actors, search_actor, search_actors
from db.movie import create_many_movies, delete_all_movies, search_movie, search_movies
from db.role import create_many_roles, delete_all_roles, search_roles
from db.script import create_many_scripts, delete_all_scripts
from db.reset_database import reset_database
from config import (
    PRO_IMDB_MOV_ROL_FILE_PATH,
    PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH,
)


async def init_database():
    """
    Initialize the database by deleting the existing posts and processed_posts and inserting the articles from the files into the database
    """
    await reset_database()

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

    res = await create_many_actors(actors)

    print(f"Inserted {res} actors")


async def insert_movies():
    """
    Insert all movies into the database
    """
    df = pd.read_csv(PRO_IMDB_MOV_ROL_FILE_PATH)

    movies = df[["title", "imdb_movie_id"]].drop_duplicates()
    movies.columns = ["title", "imdbId"]  # Rename columns
    movies = movies.to_dict("records")

    res = await create_many_movies(movies)

    print(f"Inserted {res} movies")


async def apply_async_movies(df):
    titles = df["title"].tolist()
    title_to_id = await search_movies(titles)
    return [title_to_id[title] for title in titles]


async def apply_async_actors(df):
    names = df["actor"].tolist()
    name_to_id = await search_actors(names)
    return [name_to_id[name] for name in names]


async def apply_async_roles(df):
    titles = df["role"].tolist()
    title_to_id = await search_roles(titles)
    return [title_to_id[title] for title in titles]


async def insert_roles():
    """
    Insert all roles into the database
    """
    df = pd.read_csv(PRO_IMDB_MOV_ROL_FILE_PATH)

    roles = df[
        ["title", "imdb_movie_id", "actor", "imdb_actor_id", "role"]
    ].drop_duplicates()

    # add database movieId with search_movie function
    roles["db_movie_id"] = await apply_async_movies(roles)
    roles["db_actor_id"] = await apply_async_actors(roles)

    # select only the columns we need
    roles = roles[["role", "db_movie_id", "db_actor_id"]]

    # Rename columns
    roles.columns = ["name", "movieId", "actorId"]
    roles = roles.to_dict("records")

    # columns to fill: name, movieId, actorId
    res = await create_many_roles(roles)

    print(f"Inserted {res} roles")


async def insert_scripts():
    """
    Insert all scripts into the database
    """
    df = pd.read_csv(PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH)

    scripts = df[["title", "dialogueText", "role"]].drop_duplicates()

    # add database movieId with search_movie function
    scripts["db_movie_id"] = await apply_async_movies(scripts)
    scripts["db_role_id"] = await apply_async_roles(scripts)

    # only select the columns we need: dialogueText, db_movie_id', db_role_id
    scripts = scripts[["dialogueText", "db_movie_id", "db_role_id"]]

    # Rename columns
    scripts.columns = ["dialogue", "movieId", "roleId"]

    scripts = scripts.to_dict("records")

    # columns to fill: dialogue, movieId, roleId
    res = await create_many_scripts(scripts)

    print(f"Inserted {res} scripts")


if __name__ == "__main__":
    asyncio.run(init_database())
