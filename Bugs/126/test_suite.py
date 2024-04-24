import os
import json

def run_buggy():
    os.system('python buggy/src/1_single_hidden_layer.py')

def run_fixed():
    os.system('python fixed/src/1_single_hidden_layer.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 0.05

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 0.05
