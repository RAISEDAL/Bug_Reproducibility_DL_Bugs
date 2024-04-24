import os
import pytest

def run_buggy():
    os.system('cd buggy;python main.py')

def run_fixed():
    os.system('cd fixed;python main.py')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()