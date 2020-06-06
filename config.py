import yaml
import os 
    
def set_defaults(config):
    pass

def load(cfg_path):
    assert(os.path.exists(cfg_path))
    with open(cfg_path) as cfg_file:
        config = yaml.safe_load(cfg_file)
    set_defaults(config)    
    return config

def save(config, cfg_path):
    with open(cfg_path, "w") as cfg_file:
        yaml.dump(config, cfg_file, default_flow_style=False)