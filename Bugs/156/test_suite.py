import os
import pytest

def run_buggy():
    os.system('python buggy/lab-06-1-softmax_classifier.py')

def run_fixed():
    os.system('python fixed/lab-06-1-softmax_classifier.py')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()
        raise
