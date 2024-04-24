import os
import json

def run_buggy():
    os.system('cd buggy;python keras_catsdogs.py')

def run_fixed():
    os.system('cd fixed;python keras_catsdogs.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.7

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.7
