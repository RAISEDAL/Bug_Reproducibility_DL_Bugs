import os
import json

def run_buggy():
    os.system('python buggy/autoencoder/VariationalAutoencoderRunner.py')

def run_fixed():
    os.system('python fixed/autoencoder/VariationalAutoencoderRunner.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    cost = result.get('cost')
    assert type(cost) is float

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    cost = result.get('cost')
    assert type(cost) is float
