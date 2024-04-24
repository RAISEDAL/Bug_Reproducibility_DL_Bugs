import os
import json

def run_buggy():
    os.system('python buggy/cifar10-cnn.py')

def run_fixed():
    os.system('python fixed/cifar10-cnn.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.8

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.8
