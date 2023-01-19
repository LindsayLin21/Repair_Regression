import pathlib
import random

import numpy as np
import torch
import yacs.config

def save_config(config: yacs.config.CfgNode,
                output_path: pathlib.Path) -> None:
    with open(output_path, 'w') as f:
        f.write(str(config))

def load_checkpoint(path, device):
    model = torch.load(path, map_location=device)
    return model