from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from pprint import pprint

model_name = "zbnsl/bert-base-uncased-emotionsModified"

# Download and load the model and tokenizer locally
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

# Initialize the pipeline with the local model and tokenizer
classifier = pipeline(
    task="text-classification", model=model, tokenizer=tokenizer, top_k=None
)

# Input sentences for classification
sentences = [
    "I am happy",
]

# Perform classification
model_outputs = classifier(sentences)
pprint(model_outputs)
