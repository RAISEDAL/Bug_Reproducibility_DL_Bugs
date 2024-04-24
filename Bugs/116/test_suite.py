import os
import pytest

def run_buggy():
    os.system('cd buggy; ./download_data.sh')
    os.system('cd buggy; python prediction_train.py --output_dir=./checkpoints')

def run_fixed():
    os.system('cd fixed; ./download_data.sh')
    os.system('cd fixed; python prediction_train.py --output_dir=./checkpoints')

def test_buggy():
    with pytest.raises(Exception) as e_info:
        run_buggy()

def test_fixed():
    with pytest.raises(Exception) as e_info:
        run_fixed()