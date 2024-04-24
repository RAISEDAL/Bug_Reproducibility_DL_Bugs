import os
import json

def run_buggy():
    os.system('python buggy/lab-09-4-xor_tensorboard.py')

def run_fixed():
    os.system('python fixed/lab-09-4-xor_tensorboard.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy == 1.0

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy == 1.0
