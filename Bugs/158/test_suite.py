import os
import pytest

def run_buggy():
    os.system('python buggy/klab-04-2-multi_input_linear_regression.py')

def run_fixed():
    os.system('python fixed/klab-04-2-multi_input_linear_regression.py')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()
        

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()
        raise
