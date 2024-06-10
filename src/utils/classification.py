from typing import List
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import globals


def load_classification_model() -> pipeline:
    """
    Load the classification model and tokenizer from the Hugging Face model hub
    """
    model_name = "zbnsl/bert-base-uncased-emotionsModified"

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    # Initialize the pipeline with the local model and tokenizer
    globals._classifier = pipeline(
        task="text-classification", model=model, tokenizer=tokenizer, top_k=None
    )
    return globals._classifier


def get_classification(text: List[str]) -> List[dict]:
    """
    Perform text classification using the loaded model
    """
    if globals._classifier is None:
        globals._classifier = load_classification_model()

    # Perform classification
    return globals._classifier(text)
