from imdb import Cinemagoer
import os
import sys
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import RAW_IMSDB_MOV_FILE_PATH, PRO_IMDB_MOV_ROL_FILE_PATH


def fetch_movie_data(movie_name, ia):
    """Fetches movie data from IMDb for a given movie title."""
    movies = ia.search_movie(movie_name)
    characters_data = []

    if movies:
        movie = movies[0]
        ia.update(movie)
        movie_id = movie.movieID

        for person in movie.get("cast", []):
            characters = person.currentRole
            if not isinstance(characters, list):
                characters = [characters]

            for character in characters:
                if "name" in character:
                    characters_data.append(
                        {
                            "title": movie["title"],
                            "imdb_movie_id": movie_id,
                            "actor": person["name"],
                            "imdb_actor_id": person.personID,
                            "role": character["name"],
                        }
                    )
                else:
                    print(
                        f"Warning: Actor '{person['name']}' without a role name found in movie '{movie['title']}'"
                    )
    return characters_data


def get_imdb_data(input_file_path: str, output_file_path: str):
    """Fetches IMDb data for movies listed in a CSV file and saves the character data to another CSV file."""
    ia = Cinemagoer()
    df = pd.read_csv(input_file_path)
    unique_titles = df["title"]

    characters_data = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(fetch_movie_data, movie_name, ia): movie_name
            for movie_name in unique_titles
        }
        for future in tqdm(
            as_completed(futures), total=len(futures), desc="Processing Movies"
        ):
            try:
                result = future.result()
                characters_data.extend(result)
            except Exception as exc:
                movie_name = futures[future]
                print(f"Error processing {movie_name}: {exc}")

    characters_df = pd.DataFrame(characters_data)
    characters_df.to_csv(output_file_path, index=False)


if __name__ == "__main__":
    get_imdb_data(RAW_IMSDB_MOV_FILE_PATH, PRO_IMDB_MOV_ROL_FILE_PATH)
