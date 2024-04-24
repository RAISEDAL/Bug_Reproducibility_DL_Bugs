import os
import json

def run_buggy():
    os.system('cd buggy/LeNet/Keras;python main.py')

def run_fixed():
    os.system('cd fixed/LeNet/Keras;python main.py')

def test_buggy():
    run_buggy()
    file = open(file="buggy/LeNet/Keras/result.json", mode='r')
    result = json.load(file)
    acc = result.get('val_acc')
    assert acc >= 0.467

def test_fixed():
    run_fixed()
    file = open(file="fixed/LeNet/Keras/result.json", mode='r')
    result = json.load(file)
    acc = result.get('val_acc')
    assert acc >= 0.467
