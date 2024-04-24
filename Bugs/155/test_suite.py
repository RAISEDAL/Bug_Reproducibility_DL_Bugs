import os
import pytest

def run_buggy():
    os.system('python buggy/conv_filter_visualization.py')

def run_fixed():
    os.system('python fixed/conv_filter_visualization.py')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()
