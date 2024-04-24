import os
import json

def run_buggy():
    os.system('python buggy/command_line/run_dbn.py')

def run_fixed():
    os.system('python fixed/command_line/run_dbn.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.11

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.11
