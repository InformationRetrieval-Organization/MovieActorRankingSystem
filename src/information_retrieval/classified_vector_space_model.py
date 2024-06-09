import math
from typing import Any, List
import numpy as np
from db.actor import get_all_actors, get_all_actors_dialogues_processed
from db.script import get_all_scripts
from db.role import get_all_roles
import globals
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
from prisma import models
from db.actor_classifier import get_all_actor_classifiers


async def search_classified_vector_space_model(query: List[str]) -> List[int]:
    """
    Creates the Queryvector and calculates the cosine similiarity between the Queryvector and the Actor vectors
    """

    # Get synonyms for the query terms

    # Classify query with synonyms

    # Calculate vector for query with classification

    # Calculate cosine similarity between query vector and actor vectors

    # Return actors with highest cosine similarity


async def build_classified_vector_space_model():
    """
    Calculate the vectors for every actor based on their classification
    """

    print("Building classified vector space model")
    # Get all classified actors
    classified_actors = await get_all_actor_classifiers()
    # Caculate vectors for each actor
    for actor in tqdm(classified_actors):
        # Calculate the vector for the actor
        vector = calculate_actor_vector(actor)
        globals._classified_actors_vector_map[actor.id] = vector

    print("Building classified vector space model completed")


def calculate_actor_vector(actor: models.ActorClassifier) -> List[float]:
    """
    Read the values for the classification and calculate the vector for the actor
    """
    vector = []
    vector.append(actor.angerScore)
    vector.append(actor.fearScore)
    vector.append(actor.joyScore)
    vector.append(actor.sadnessScore)
    vector.append(actor.loveScore)
    vector.append(actor.surpriseScore)
    return vector
