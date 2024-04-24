import os
import pytest

def run_buggy():
    os.system('python buggy/gated_pixelcnn/train_mnist.py')

def run_fixed():
    os.system('python fixed/gated_pixelcnn/train_mnist.py')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()
