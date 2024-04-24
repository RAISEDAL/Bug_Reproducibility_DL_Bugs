import os
import json

def run_buggy():
    os.system('python buggy/pix2pix_train.py')

def run_fixed():
    os.system('python fixed/pix2pix_train.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    ellapsed_time = result.get('ellapsed_time')
    assert ellapsed_time <= 600

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    ellapsed_time = result.get('ellapsed_time')
    assert ellapsed_time <= 600
