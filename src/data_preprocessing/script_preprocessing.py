import re
from typing import Dict, List, Set, Tuple
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from prisma import models
from db.script import (
    get_all_scripts,
    update_one_script,
)
import globals


async def preprocess_scripts():
    """
    Preprocesses the scripts in the database and returns a list of tokens.
    """
    print("Start Preprocessing")

    download_nltk_resources()

    # Get the scripts from the database
    scripts = await get_all_scripts()
    processed_scripts = [
        script for script in scripts if script.processedDialogue
    ]  # get all scripts that are already preprocessed

    if len(scripts) != len(processed_scripts):
        # Preprocess the scripts
        print("Not all scripts are preprocessed, start preprocessing:")
        new_processed_scripts, list_of_tokens = await preprocess_and_update_scripts(
            scripts - processed_scripts
        )
        processed_scripts.extend(new_processed_scripts)
    else:
        # all scripts are already preprocessed
        print("Scripts are already preprocessed")
        list_of_tokens = await calculate_vocabulary(processed_scripts)

    _vocabulary = list_of_tokens

    print(str(len(processed_scripts)) + " scripts came trough the preprocessing")
    print("Length of Vocabulary: " + str(len(_vocabulary)))
    print("Preprocessing completed")


def download_nltk_resources():
    """
    Download the necessary NLTK resources.
    """
    nltk.download("punkt")
    nltk.download("wordnet")
    nltk.download("stopwords")
    nltk.download("words")


def handle_tokens(term_freq_map: Dict[str, int], tokens: List[str]) -> List[str]:
    """
    Handle tokens: filter out unique tokens.
    """
    # Find tokens that occur only once
    unique_tokens = [key for key, value in term_freq_map.items() if value == 1]
    tokens = [token for token in tokens if token not in unique_tokens]

    # Remove duplicates
    tokens = list(set(tokens))
    return tokens


async def preprocess_and_update_scripts(
    scripts: List[models.Script],
) -> Tuple[List[models.Script], List[str]]:
    """
    Preprocesses the posts and inserts them into the database.
    """
    # Initialize the variables
    list_of_tokens = []
    processed_scripts = []
    term_freq_map = {}

    english_words = set(nltk.corpus.words.words())

    for script in scripts:
        # Preprocess the script
        processed_script, tokens = preprocess_script(script, english_words)

        if not processed_script:  # if the processed_script is empty
            continue

        # Add to processed_script list
        processed_scripts.append(processed_script)

        set_term_freq_map(term_freq_map, tokens)

        list_of_tokens.extend(tokens)

    list_of_tokens = handle_tokens(term_freq_map, list_of_tokens)

    # update the script in the datebase
    for processed_script in processed_scripts:
        await update_one_script(processed_script)

    return processed_scripts, list_of_tokens


async def calculate_vocabulary(processed_scripts: List[models.Script]) -> List[str]:
    """
    Calculates the date coefficients and vocabulary for the processed posts.
    """
    list_of_tokens = []
    term_freq_map = {}

    for processed_script in processed_scripts:
        # Tokenize the processed script dialouge
        tokens = processed_script.processedDialogue.split()

        set_term_freq_map(term_freq_map, tokens)

        # Add the tokens to the list of tokens
        list_of_tokens.extend(tokens)

    list_of_tokens = handle_tokens(term_freq_map, list_of_tokens)

    return list_of_tokens


def preprocess_script(
    script: models.Script, english_words: Set[str]
) -> Tuple[models.Script, List[str]]:
    """
    Preprocess a script.
    """
    # Remove special characters and convert to lowercase
    content = script.title.lower() + " " + script.content.lower()  # Add the title
    content = re.sub("[–!\"#$%&'()*+,-./:;<=‘>—?@[\]^_`�{|}~\n’“”]", "", content)

    # Remove non-english words
    content = " ".join(
        w
        for w in nltk.wordpunct_tokenize(content)
        if w.lower() in english_words or not w.isalpha()
    )

    # Tokenize the script
    tokens = word_tokenize(content)

    # Remove stopwords
    stop_words = set(stopwords.words("english"))
    tokens = [token for token in tokens if token not in stop_words]

    # Lemmatize the tokens
    lemmatizer = nltk.stem.WordNetLemmatizer()
    tokens = [lemmatizer.lemmatize(token) for token in tokens]

    # Create the processed script
    processed_script = script
    processed_script.processedDialogue = " ".join(tokens)

    return processed_script, tokens


def set_term_freq_map(term_freq_map: Dict[str, int], tokens: List[str]) -> None:
    """
    Set the term frequency map for a script.
    """
    for token in tokens:
        if token in term_freq_map:
            term_freq_map[token] += 1
        else:
            term_freq_map[token] = 1
