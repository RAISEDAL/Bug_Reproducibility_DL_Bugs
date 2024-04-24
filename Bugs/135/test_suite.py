import os
import json

def run_buggy():
    os.system('cd buggy;python train.py')

def run_fixed():
    os.system('cd fixed;python train.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 0.1

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 0.1
