import os

import yaml

from helpers.constants.framework_constants import CONFIG_YAML


def load_config():
    config_path = os.path.join(os.path.dirname(__file__), CONFIG_YAML)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    return {}