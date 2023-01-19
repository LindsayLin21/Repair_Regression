import pathlib
import random

import numpy as np
import torch
import yacs.config

from src.config.config_node import ConfigNode
from src import get_default_config

# Format time for printing purposes
def get_hms(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)

    return h, m, s

def set_seed(config: yacs.config.CfgNode) -> None:
    seed = config.train.seed
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)


def setup_cudnn(config):
    torch.backends.cudnn.benchmark = config.cudnn.benchmark
    torch.backends.cudnn.deterministic = config.cudnn.deterministic

def save_config(config, output_path):
    with open(output_path, 'w') as f:
        f.write(str(config))


def get_env_info(config):
    info = {
        'pytorch_version': str(torch.__version__),
        'cuda_version': torch.version.cuda or '',
        'cudnn_version': torch.backends.cudnn.version() or '',
    }
    if config.device != 'cpu':
        info['num_gpus'] = torch.cuda.device_count()
        info['gpu_name'] = torch.cuda.get_device_name(0)
        capability = torch.cuda.get_device_capability(0)
        info['gpu_capability'] = f'{capability[0]}.{capability[1]}'

    return ConfigNode({'env_info': info})

def find_config_diff(config):
    def _find_diff(node, default_node):
        root_node = ConfigNode()
        for key in node:
            val = node[key]
            if isinstance(val, yacs.config.CfgNode):
                new_node = _find_diff(node[key], default_node[key])
                if new_node is not None:
                    root_node[key] = new_node
            else:
                if node[key] != default_node[key]:
                    root_node[key] = node[key]
        return root_node if len(root_node) > 0 else None

    default_config = get_default_config()
    new_config = _find_diff(config, default_config)
    return new_config