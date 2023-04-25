import os
import random
import numpy as np
import torch


def fix_seeds(seed=42):
    assert os.environ["PYTHONHASHSEED"] == str(seed), f"set: PYTHONHASHSEED={seed}"
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True