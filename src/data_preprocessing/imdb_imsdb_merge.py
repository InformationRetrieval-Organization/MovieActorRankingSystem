import pandas as pd
import os
import sys
from fuzzywuzzy import fuzz
from tqdm import tqdm
import concurrent.futures

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import (
    PRO_IMDB_MOV_ROL_FILE_PATH,
    PRO_IMSDB_MOV_SCR_FILE_PATH,
    PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH,
)


def process_dialogue_row(dialogue_row, imdb_movies):
    """
    Process a single dialogue row and find the best match for the role using fuzzy string matching.
    """
    movie_title = dialogue_row["movie"]
    dialogue_role = dialogue_row["role"]
    dialogue_text = dialogue_row["dialogueText"]

    # Filter the imdb_movies dataframe for the current movie title
    movie_matches = imdb_movies[imdb_movies["title"] == movie_title]

    if not movie_matches.empty:
        # Find the best match for the role using fuzzy string matching
        best_match = None
        highest_score = 0

        for _, movie_row in movie_matches.iterrows():
            imdb_role = movie_row["role"]
            score = fuzz.partial_ratio(dialogue_role, imdb_role)

            if score > highest_score:
                highest_score = score
                best_match = movie_row

        # If a match is found with a score above a threshold, return the merged data
        if (
            best_match is not None and highest_score >= 30
        ):  # Adjust the threshold as needed
            return {
                "title": movie_title,
                "imdb_id": best_match["imdb_movie_id"],
                "dialogueText": dialogue_text,
                "actor": best_match["actor"],
                "actor_id": best_match["imdb_actor_id"],
                "role": best_match["role"],
            }
    return None


def merge_movie_data(
    pro_imdb_mov_rol_file_path, pro_imsdb_mov_scr_file_path, output_file_path
):
    """
    Merge the movie and role dataframes based on partial string matching for the role.
    """
    # Read the CSV files
    imdb_movies = pd.read_csv(pro_imdb_mov_rol_file_path)
    imsdb_movie_dialogues = pd.read_csv(pro_imsdb_mov_scr_file_path)

    # Initialize a list to store the merged data
    merged_data = []

    # Use ThreadPoolExecutor to process dialogue rows in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(
                process_dialogue_row, dialogue_row, imdb_movies
            ): dialogue_row
            for _, dialogue_row in imsdb_movie_dialogues.iterrows()
        }

        for future in tqdm(
            concurrent.futures.as_completed(futures),
            total=len(futures),
            desc="Processing IMSDB/IMDB Data",
        ):
            result = future.result()
            if result is not None:
                merged_data.append(result)

    # Convert the merged data to a DataFrame
    merged_df = pd.DataFrame(merged_data)

    # Save the merged DataFrame to a CSV file
    merged_df.to_csv(output_file_path, index=False)

    return merged_df


if __name__ == "__main__":
    merged_df = merge_movie_data(
        PRO_IMDB_MOV_ROL_FILE_PATH,
        PRO_IMSDB_MOV_SCR_FILE_PATH,
        PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH,
    )

    print("Merged data saved to:", PRO_IMDB_IMSDB_MOV_SCR_FILE_PATH)
