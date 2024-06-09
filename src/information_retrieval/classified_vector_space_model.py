import math
from typing import Any, List
import numpy as np
from db.actor import get_all_actors, get_all_actors_dialogues_processed
from db.script import get_all_scripts
from db.role import get_all_roles
import globals
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor
import os
from prisma import models
from db.actor_classifier import get_all_classified_actors


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
    # Get all classified actors
    classified_actors = await get_all_classified_actors()
    # Caculate vectors for each actor
