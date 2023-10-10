"""XXX"""
import os
import json
#import tkinter
import spacy
from numpy import mean

from parse_input import parse_input

DIR = os.path.dirname(__file__)
SCENE = os.path.join(DIR, "locked_room.json")
FLAG = True
ACCURACY = 0.7
SPEECH_LIST = ["advmod", "nsubj"]
nlp = spacy.load("en_core_web_lg")


def load_scene(scene:__file__, input_type:str) -> dict:
    """Returns a dictionary from .json file.
    All keys and values in dictionary are nlp objects.
    """
    with open(scene, "r", encoding="utf-8-sig") as file:
        data = json.load(file)
    return {nlp(x):[nlp(y) for y in data[input_type][x]] for x in data[input_type]}


def chatbot(sentence:str):
    """XXX""" 
    sentence = parse_input(sentence)
    # Break up data so that 'values' can be compared.
    if "question" in sentence:
        data = load_scene(SCENE, "question")
        temp = 'question'
    elif "request" in sentence:
        return "I don't do requests. I only answer questions."

    key_list = list(data.keys())    # Responses
    val_list = list(data.values())  # Keywords matching a response.
    # Determine best response.
    for i,sub_list in enumerate(val_list):
        for j,token in enumerate(sub_list):
            val_list[i][j] = token.similarity(sentence[temp])

    response = [mean(x) for x in val_list]  # list of response similarities
    # Check if best response is a valid response
    if max(response) >= ACCURACY:
        response = key_list[response.index(max(response))]  # Best response as text
        return "".join(response.text)
    return "That makes no sense"



#------------------------------UNIT TEST-------------------------------

if __name__  == "__main__":
    print("Hi there. My name is ChatBot. I am a Chat bot. Hence, the name. What is your name?")
    while FLAG:
        user_input = input("ME: ")
        print("??:",chatbot(user_input))
    print("Congratulations, you are free!")
