import os
import json

def run_buggy():
    os.system('python buggy/transformer/cluttered_mnist.py')

def run_fixed():
    os.system('python fixed/transformer/cluttered_mnist.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 1

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 1
