import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from utils.classification import load_classification_model, get_classification


first_sentence = "I love you, you are the best person in the world. I love you, you are the best person in the world. I love you, you are the best person in the world.I love you, you are the best person in the world. v v v I love you, you are the best person in the world."
second_sentence = "I hate you, you are the worst person in the world. I hate you, you are the worst person in the world. I hate you, you are the worst person in the world. I hate you, you are the worst person in the world. I hate you, you are the worst person in the world. I hate you, you are the worst person in the world. I hate you, you are the worst person in the world."

load_classification_model()


def get_score(sentences, label):
    for sentence in sentences:
        if sentence["label"] == label:
            return sentence["score"]
    return None


# first, classify with two seperate sentences
first = get_classification([first_sentence])
second = get_classification([second_sentence])

print("First sentence, loveScore: ", get_score(first[0], "love"))
print("Second sentence, loveScore: ", get_score(second[0], "love"))

# calculate median score
median_score = (get_score(first[0], "love") + get_score(second[0], "love")) / 2
print("First and Second median: ", median_score)

# then, classify with both sentences combined
combined = get_classification([first_sentence + " " + second_sentence])
print("Combined sentence, loveScore: ", get_score(combined[0], "love"))
