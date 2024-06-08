from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from prisma import models
from db.script import get_all_scripts
from db.actor import get_all_actors
from db.role import get_all_roles
from db.actor_classifier import create_one_actor_classifier
import globals


def load_classification_model() -> pipeline:
    model_name = "zbnsl/bert-base-uncased-emotionsModified"

    # Download and load the model and tokenizer locally
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Initialize the pipeline with the local model and tokenizer
    globals._classifier = pipeline(
        task="text-classification", model=model, tokenizer=tokenizer, top_k=None
    )
    return globals._classifier


def get_classification(text: List[str]):
    if globals._classifier == None:
        globals._classifier = load_classification_model()

    # Perform classification
    return globals._classifier(text)


async def classify_actors():
    # Get all scripts, roles and actors from the database
    scripts = await get_all_scripts()
    roles = await get_all_roles()
    actors = await get_all_actors()

    actors_classification = {}  # dictionary to store the classification of each actor

    # iterate over all actors
    for actor in actors:
        if actor.id <= 1534:  # Continue where last execution stopped
            continue
        actor_roles = [role for role in roles if role.actorId == actor.id]

        # lists for the values of each classification
        actor_sadness = []
        actor_joy = []
        actor_anger = []
        actor_fear = []
        actor_surprise = []
        actor_love = []

        done = 0
        # iterate over all roles of the actor
        for role in actor_roles:
            # get all scripts of the role
            role_scripts = []
            for script in scripts:
                if script.roleId == role.id:
                    len_of_script = len(script.dialogue)
                    if len_of_script > 512:
                        script.dialogue = script.dialogue[:512]
                    role_scripts.append(script.dialogue)

            # get the classification of the role scripts
            classification = get_classification(role_scripts)

            # iterate over the classification and store in the corresponding lists
            for i in range(len(classification)):
                for j in range(len(classification[i])):
                    if classification[i][j]["label"] == "sadness":
                        actor_sadness.append(classification[i][j]["score"])
                    elif classification[i][j]["label"] == "joy":
                        actor_joy.append(classification[i][j]["score"])
                    elif classification[i][j]["label"] == "anger":
                        actor_anger.append(classification[i][j]["score"])
                    elif classification[i][j]["label"] == "fear":
                        actor_fear.append(classification[i][j]["score"])
                    elif classification[i][j]["label"] == "surprise":
                        actor_surprise.append(classification[i][j]["score"])
                    elif classification[i][j]["label"] == "love":
                        actor_love.append(classification[i][j]["score"])

        # calculate the average value of each classification
        actor_sadness_value = (
            sum(actor_sadness) / len(actor_sadness) if len(actor_sadness) > 0 else 0
        )
        actor_joy_value = sum(actor_joy) / len(actor_joy) if len(actor_joy) > 0 else 0
        actor_anger_value = (
            sum(actor_anger) / len(actor_anger) if len(actor_anger) > 0 else 0
        )
        actor_fear_value = (
            sum(actor_fear) / len(actor_fear) if len(actor_fear) > 0 else 0
        )
        actor_surprise_value = (
            sum(actor_surprise) / len(actor_surprise) if len(actor_surprise) > 0 else 0
        )
        actor_love_value = (
            sum(actor_love) / len(actor_love) if len(actor_love) > 0 else 0
        )

        # store the classification in the dictionary
        actors_classification[actor.id] = {
            "sadness": actor_sadness_value,
            "joy": actor_joy_value,
            "anger": actor_anger_value,
            "fear": actor_fear_value,
            "surprise": actor_surprise_value,
            "love": actor_love_value,
        }
        # Create entry in DB
        await create_one_actor_classifier(
            actor_id=actor.id,
            love_score=actors_classification[actor.id]["love"],
            joy_score=actors_classification[actor.id]["joy"],
            anger_score=actors_classification[actor.id]["anger"],
            sadness_score=actors_classification[actor.id]["sadness"],
            surprise_score=actors_classification[actor.id]["surprise"],
            fear_score=actors_classification[actor.id]["fear"],
        )
        done += 1
        percentage = (done / len(actors)) * 100
        print(f"Actor {actor.id} classified successfully. Progress: {percentage}%")
