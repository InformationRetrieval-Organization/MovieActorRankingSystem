from datetime import datetime
from typing import Dict, List, Union
from prisma import models, Prisma


async def get_all_movies() -> List[models.Movie]:
    """
    Fetch all movies from the database
    """
    try:
        async with Prisma() as db:
            return await db.movie.find_many()
    except Exception as e:
        print(f"An error occurred while fetching movies: {e}")
        return []


async def create_many_movies(movies: List[Dict[str, Union[str, int]]]) -> int:
    """
    Create multiple movies in the database
    """
    try:
        async with Prisma() as db:
            result = await db.movie.create_many(data=movies)
            return result
    except Exception as e:
        print(f"An error occurred while creating the movies: {e}")


async def create_one_movie(title: str, imdb_id: int, cover_url: str) -> models.Movie:
    """
    Create a movie in the database
    """
    try:
        async with Prisma() as db:
            movie = await db.movie.create(
                data={
                    "title": title,
                    "imdbId": imdb_id,
                    "coverUrl": cover_url,
                }
            )
            return movie
    except Exception as e:
        print(f"An error occurred while creating the movie: {e}")


async def delete_all_movies() -> None:
    """
    Delete all movies from the database and reset the auto-increment counter
    """
    print("Deleting all movies")
    try:
        async with Prisma() as db:
            # await db.movie.delete_many()
            # await db.execute_raw('TRUNCATE TABLE "Movie" RESTART IDENTITY')
            await db.execute_raw('TRUNCATE TABLE "Movie" RESTART IDENTITY CASCADE')
    except Exception as e:
        print(f"An error occurred while deleting movies: {e}")


async def search_movie(title: str) -> List[models.Movie]:
    """
    Search for a movie by title
    """
    try:
        async with Prisma() as db:
            return await db.movie.find_many(where={"title": {"contains": title}})
    except Exception as e:
        print(f"An error occurred while searching for the movie: {e}")
        return []


async def search_movies(titles: List[str]) -> Dict[str, int]:
    """
    Search for movies by titles
    """
    try:
        async with Prisma() as db:
            movies = await db.movie.find_many(where={"title": {"in": titles}})
            return {movie.title: movie.id for movie in movies}
    except Exception as e:
        print(f"An error occurred while searching for the movies: {e}")
        return {}
