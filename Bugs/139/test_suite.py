import os
import json

def run_buggy():
    os.system('python buggy/examples/03_logistic_regression_mnist_sol.py')

def run_fixed():
    os.system('python fixed/examples/03_logistic_regression_mnist_sol.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.9175

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    accuracy = result.get('accuracy')
    assert accuracy >= 0.9175
