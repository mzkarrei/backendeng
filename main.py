
import json


"""
    Load the main functions and the model functions
"""

from src.functions.functions import load_genotypes
from src.model.model import run


CONFIG_FILE = "config.json"

# Load Config file
def load_config(path = CONFIG_FILE):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception as e:
        raise RuntimeError(f"Failed to load config file {path}: {e}") from e


def main(config):

    # Load required files 
    # 1. Load Genotypes
    # 2. Load Phenotypes 

    # Run the model and capture result

    # Save the result
    pass

if __name__ == "__main__":
    try:
        config = load_config(CONFIG_FILE)
        main(config)
    except Exception as e:
        raise e