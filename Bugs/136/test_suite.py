import os
import json

def run_buggy():
    os.system('cd buggy/src/generation;python process.py;python learn.py')

def run_fixed():
    os.system('cd fixed/src/generation;python process.py;python learn.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/src/generation/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 0.3

def test_fixed():
    run_fixed()
    file = open(file="fixed/src/generation/result.json", mode='r')
    result = json.load(file)
    loss = result.get('loss')
    assert loss <= 0.3
