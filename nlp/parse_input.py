"""XXX"""

import os
import json
import warnings
import spacy
from spacy.matcher import Matcher
DIR = os.path.dirname(__file__)
PATTERNS = os.path.join(DIR, "patterns.json")

warnings.filterwarnings("ignore", message=r"\[W008\]", category=UserWarning)
nlp = spacy.load("en_core_web_lg")


def import_patterns(pattern_type):
    """XXX""" 
    with open(PATTERNS, "r", encoding="utf-8") as file:
        data = json.load(file)
    return list(data[pattern_type])


def parse_input(sentence):
    """XXX""" 
    sentence = nlp(sentence)
    input_type = determine_type(sentence) or ["type", ""]
    input_target = determine_target(sentence) or ["target", ""]
    input_action = determine_action(sentence) or ["action", ""]
    return {
        input_type[0]: nlp(input_type[1]),
        input_target[0]: nlp(input_target[1]),
        input_action[0]: nlp(input_action[1])
        }


def determine_type(sentence):
    """XXX""" 
    matcher = Matcher(nlp.vocab, validate=True)
    matcher.add("request", import_patterns("pattern_request"))
    matcher.add("question", import_patterns("pattern_question"))
    matches = matcher(sentence)
    if matches:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = sentence[start:end]  # The matched span
            return [string_id, span.text]
    return None


def determine_target(sentence):
    """XXX""" 
    matcher = Matcher(nlp.vocab, validate=True)
    matcher.add("target", import_patterns("pattern_target"))
    matches = matcher(sentence)
    if matches:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = sentence[start:end]  # The matched span
            return [string_id, span.text]
    return None


def determine_action(sentence):
    """XXX""" 
    matcher = Matcher(nlp.vocab, validate=True)
    matcher.add("action", import_patterns("pattern_action"))
    matches = matcher(sentence)
    if matches:
        for match_id, start, end in matches:
            string_id = nlp.vocab.strings[match_id]  # Get string representation
            span = sentence[start:end]  # The matched span
            return [string_id, span.text]
    return None
#------------------------------UNIT TEST-------------------------------

if __name__  == "__main__":
    while True:
        request = input("TEST: ")
        print("dep_: ", " ".join(x.dep_ for x in nlp(request)), end="")
        print()
        print("lem_: ", " ".join(x.lemma_ for x in nlp(request)), end="")
        print()
        print("tag_: ", "; ".join(spacy.explain(x.tag_) for x in nlp(request)), end="")
        print()
        print("ent_: ", " ".join(x.text for x in nlp(request).ents), end="")
        print()
        print("pos_: ", " ".join(x.pos_ for x in nlp(request)), end="")
        print("\n")
        print("RETURN:",parse_input(request))
        print("------------------------")
