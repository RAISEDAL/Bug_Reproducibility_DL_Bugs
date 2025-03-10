import os
import json

def run_buggy():
    os.system('python buggy/command_line/run_logistic_regression.py')

def run_fixed():
    os.system('python fixed/command_line/run_logistic_regression.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.5

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.5
