import math
from typing import Any, List, Dict
import numpy as np
from db.actor import (
    get_actors_by_ids,
)
import globals
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from prisma import models
from db.actor_classifier import get_all_actor_classifiers
from db.actor import get_actors_by_most_roles
from nltk.corpus import wordnet as wn
from db.actor_classifier import get_all_actor_classifiers
from utils.classification import get_classification
from config import MAX_FAME_COEFFICIENT, MIN_FAME_COEFFICIENT


async def search_classified_vector_space_model(query: List[str]) -> List[int]:
    """
    Creates the Queryvector and calculates the cosine similiarity between the Queryvector and the Actor vectors
    """
    # Get synonyms for the query terms
    query_synonyms = []
    query_synonyms.append(query)
    # for term in query:
    # query_synonyms.extend(get_some_word_synonyms(term))
    # classify the query
    query_classification_map = await classify_query(query_synonyms)

    # create the query vector
    query_vector = compute_query_vector(query_classification_map)

    # Calculate cosine similarity between the query vector and actor vectors
    actor_cosine_similarity_map = {}
    for actor_id, vector in globals._classified_actors_vector_map.items():
        dot_product = np.dot(query_vector, vector)
        magnitude_query = np.linalg.norm(query_vector)
        magnitude_entry = np.linalg.norm(vector)
        cosine_similarity = dot_product / (magnitude_query * magnitude_entry)
        actor_cosine_similarity_map[actor_id] = cosine_similarity
    # sort cosine similarity descending
    sorted_actor_cosine_similarity_map = {
        k: v
        for k, v in sorted(
            actor_cosine_similarity_map.items(), key=lambda item: item[1], reverse=True
        )
    }
    # return the top 10 actors
    top_10_actors = await get_actors_by_ids(
        list(sorted_actor_cosine_similarity_map.keys())[:10]
    )
    return top_10_actors


async def build_classified_vector_space_model():
    """
    Calculate the vectors for every actor based on their classification
    """

    print("Building classified vector space model")
    # Get all classified actors
    classified_actors = await get_all_actor_classifiers()
    # Calculate the fame coefficient map
    fame_coefficient_map = await calculate_fame_coefficient_map()

    # Caculate vectors for each actor
    for actor in tqdm(classified_actors):
        # Calculate the vector for the actor
        vector = calculate_actor_vector(actor, fame_coefficient_map[actor.actorId])
        globals._classified_actors_vector_map[actor.actorId] = vector

    print("Building classified vector space model completed")


def calculate_actor_vector(
    actor: models.ActorClassifier, fame_coefficient: float
) -> List[float]:
    """
    Read the values for the classification and calculate the vector for the actor
    """
    vector = []

    vector.append(actor.loveScore) * fame_coefficient
    vector.append(actor.joyScore) * fame_coefficient
    vector.append(actor.angerScore) * fame_coefficient
    vector.append(actor.sadnessScore) * fame_coefficient
    vector.append(actor.surpriseScore) * fame_coefficient
    vector.append(actor.fearScore) * fame_coefficient
    return vector


def get_some_word_synonyms(word: str) -> List[str]:
    word = word.lower()
    synonyms = []
    synsets = wn.synsets(word)
    if len(synsets) == 0:
        return []
    synset = synsets[0]
    lemma_names = synset.lemma_names()
    for lemma_name in lemma_names:
        lemma_name = lemma_name.lower().replace("_", " ")
        if lemma_name != word and lemma_name not in synonyms:
            synonyms.append(lemma_name)
    return synonyms


async def classify_query(query: List[str]) -> List[Dict]:
    """
    Classify query based on their content and return a vector.
    """
    # Initialize an empty list for query classifications
    query_classifications = []

    # Get the classification results for the given query
    classifications = get_classification(query)

    for classification in classifications:
        # Initialize a dictionary to store emotional label scores for each classification
        label_scores = {
            "love": [],
            "joy": [],
            "anger": [],
            "sadness": [],
            "surprise": [],
            "fear": [],
        }
        for label_score in classification:
            label = label_score["label"]
            score = label_score["score"]
            label_scores[label].append(score)
        # Append the label_scores dictionary to the query_classifications list
        query_classifications.append(label_scores)

    return query_classifications


def compute_query_vector(query_clasifications: List[Dict]) -> List[float]:

    # Initialize a dictionary to store the sum of scores for each label
    label_sum = {
        "love": 0,
        "joy": 0,
        "anger": 0,
        "sadness": 0,
        "surprise": 0,
        "fear": 0,
    }

    # Iterate through the data and compute the sum of scores for each label
    for entry in query_clasifications:
        for label, score_list in entry.items():
            label_sum[label] += sum(score_list)

    # Calculate the average for each label
    num_entries = len(query_clasifications)
    label_avg = {label: label_sum[label] / num_entries for label in label_sum}

    # Convert the label averages into a vector
    label_vector = [label_avg[label] for label in label_sum]
    return label_vector


async def calculate_fame_coefficient_map() -> Dict[int, float]:
    """
    Calculate the fame coefficient for an actor based on their classification scores.
    """

    actors_list = await get_actors_by_most_roles()
    actors_list = [actor.id for actor in actors_list]  # only store actor ids

    # Calculate the coefficient for each actor
    fame_coefficient_map = {}
    for actor_id in actors_list:
        fame_coefficient = MAX_FAME_COEFFICIENT - (
            (MAX_FAME_COEFFICIENT - MIN_FAME_COEFFICIENT)
            * actors_list.index(actor_id)
            / len(actors_list)
        )
        fame_coefficient_map[actor_id] = fame_coefficient
