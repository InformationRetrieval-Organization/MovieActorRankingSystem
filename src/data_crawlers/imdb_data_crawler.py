from imdb import Cinemagoer
import os
import sys
import pandas as pd
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import RAW_MOV_FILE_PATH, PRO_MOV_ROL_FILE_PATH


def get_imdb_data():
    ia = Cinemagoer()

    # Read the CSV file
    df = pd.read_csv(RAW_MOV_FILE_PATH)

    # Get unique movie titles
    unique_titles = df["title"]  # .unique()

    # Limit to the first 5 unique titles
    # unique_titles = unique_titles[:5]

    # Create a list to store the characters data
    characters_data = []

    # Iterate over unique movie titles with a progress bar
    for movie_name in tqdm(unique_titles, desc="Processing Movies"):
        # Search for a movie (get a list of Movie objects)
        movies = ia.search_movie(movie_name)

        # Just take the first result
        if movies:
            movie = movies[0]

            # Get the full information
            ia.update(movie)

            movie_id = movie.movieID  # Retrieve the movie ID

            for person in movie.get("cast", []):
                characters = person.currentRole

                # If characters is not a list, make it a list
                if not isinstance(characters, list):
                    characters = [characters]

                for character in characters:
                    # Check if the character has a 'name' key
                    if "name" in character:
                        # Add the character to the list
                        characters_data.append(
                            {
                                "title": movie["title"],
                                "imdb_id": movie_id,  # Include the movie ID
                                "actor": person["name"],
                                "actor_id": person.personID,  # Include the actor ID
                                "role": character["name"],
                            }
                        )
                    else:
                        print(
                            f"Warning: Actor '{person['name']}' without a role name found in movie '{movie['title']}'"
                        )

    # Convert the list to a DataFrame
    characters_df = pd.DataFrame(characters_data)

    # Save the DataFrame to a CSV file
    characters_df.to_csv(PRO_MOV_ROL_FILE_PATH, index=False)


if __name__ == "__main__":
    get_imdb_data()
