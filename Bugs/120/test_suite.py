import os
import pytest

def run_buggy():
    os.system('python buggy/example.py')

def run_fixed():
    os.system('python fixed/example.py')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()
