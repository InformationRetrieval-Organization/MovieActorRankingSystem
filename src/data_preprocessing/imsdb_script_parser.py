import pandas as pd
import re
import os
import sys
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from config import RAW_IMSDB_MOV_SCR_FILE_PATH, PRO_IMSDB_MOV_SCR_FILE_PATH


def parse_script(script: str) -> list:
    # Split data by line breaks
    script_lines = script.splitlines()

    # Remove white spaces from the beginning and end of each line
    script_lines = [line.strip() for line in script_lines if line.strip()]

    # Define the patterns to remove
    patterns_to_remove = [
        r"^\d+\.$",  # Lines with only a number followed by a dot; "1.", "2."
        r"^\([-]?\d+(, [-]?\d+)*\)$",  # Lines with text inside parentheses; "(3, 4, 5)", "(10)", "(-5313)"
        r"^\(.*\)$",  # Lines with anything inside parentheses; "(CONTINUED)", "(DISAPPOINTED)"
        r"^[A-Z\s]+:\s*(\(\d+\))?$",  # Lines with uppercase letters followed by a colon: "END ON:", "CUT TO:", "CUT BACK TO:", "CONTINUED:", "FADE OUT:", "FADE IN:", "CONTINUED: (2)"
        r"^\d{1,2}\.\d{1,2}\.\d{2,4}$",  # Lines with a date format; "12.12.12", "12.12.2012"
    ]

    # Compile the patterns into a single regex
    combined_pattern = re.compile("|".join(patterns_to_remove))

    role = None
    dialogue = []
    parsed_data = []

    # Iterate over the lines in the script
    for line in script_lines:
        if combined_pattern.match(line):
            continue

        # Remove non-letter characters and check if the line is in uppercase
        if re.sub(r"[^a-zA-Z]", "", line).isupper():
            # If there's a previous role and dialogue, save them
            if role is not None:  # dialogue is can be empty
                parsed_data.append((role, " ".join(dialogue)))

            # Start a new role and clear the dialogue
            role = line
            dialogue = []
        else:
            # Add the line to the dialogue
            dialogue.append(line)

    # Save the last role and dialogue
    if role and dialogue:
        parsed_data.append((role, " ".join(dialogue)))

    # remove stage instructions; starting with "EXT." or "INT."
    parsed_data = [
        (role, dialogue)
        for role, dialogue in parsed_data
        if not role.startswith(("EXT.", "INT.", "VFX:"))
    ]

    return parsed_data


def process_scripts(input_csv_path, output_csv_path):
    # Read the input CSV file
    df = pd.read_csv(input_csv_path)

    # Drop empty rows and rows with missing values
    df.dropna(subset=["script"], inplace=True)

    # Create a list to store the processed data
    processed_data = []

    # Iterate over each row in the DataFrame
    for index, row in tqdm(df.iterrows(), desc="Processing Scripts"):
        title = row["title"]
        script = row["script"]

        # Parse the script to extract roles and dialogues
        parsed_script = parse_script(script)

        # Add the parsed data to the processed data list
        for role, dialogue in parsed_script:
            processed_data.append(
                {"dialogueText": dialogue, "movie": title, "role": role}
            )

    # Create a new DataFrame from the processed data
    output_df = pd.DataFrame(processed_data)

    # Save the DataFrame to a new CSV file
    output_df.to_csv(output_csv_path, index=False)


# Run the script
if __name__ == "__main__":
    process_scripts(RAW_IMSDB_MOV_SCR_FILE_PATH, PRO_IMSDB_MOV_SCR_FILE_PATH)
