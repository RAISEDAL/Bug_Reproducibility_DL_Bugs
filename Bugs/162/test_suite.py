import os
import pytest

def run_buggy():
    os.system('cd buggy/ccgan;python ccgan.py')

def run_fixed():
    os.system('cd fixed/ccgan;python ccgan.py')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()
        

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()
        raise
