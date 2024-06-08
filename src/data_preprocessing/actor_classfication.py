from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pprint import pprint

classifier = None

def load_classification_model():
    model_name = "zbnsl/bert-base-uncased-emotionsModified"

    # Download and load the model and tokenizer locally
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Initialize the pipeline with the local model and tokenizer
    classifier = pipeline(
        task="text-classification", model=model, tokenizer=tokenizer, top_k=None
    )

def get_classification(text: List[str]):
    if classifier == None:
        load_classification_model()

    # Perform classification
    return classifier(text)
