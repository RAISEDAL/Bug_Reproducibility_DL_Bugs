import os
import json

def run_buggy():
    os.system('python buggy/command_line/run_rbm.py --verbose=1 --num_hidden=250 --num_epochs=10 --batch_size=128 --model_name=rbm --learning_rate=0.0001')

def run_fixed():
    os.system('python fixed/command_line/run_rbm.py --verbose=1 --num_hidden=250 --num_epochs=10 --batch_size=128 --model_name=rbm --learning_rate=0.0001')

def test_buggy():
    run_buggy()
    file = open(file="buggy/result.json", mode='r')
    result = json.load(file)
    res_len = len(result.values())
    diff = list(result.values())[res_len-2] - list(result.values())[res_len-1]
    assert diff <= 0.0025

def test_fixed():
    run_fixed()
    file = open(file="fixed/result.json", mode='r')
    result = json.load(file)
    res_len = len(result.values())
    diff = list(result.values())[res_len - 2] - list(result.values())[res_len - 1]
    assert diff <= 0.0025