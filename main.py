
import json

"""
    Load the main functions and the model functions
"""

from src.functions.functions import load_genotypes, load_phenotype, export_results
from src.model.model import run

LOG = True
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
    genotypes = load_genotypes(GENO_FILE=config["GENOTYPES_FILE"])
    print(genotypes)

    # For each genotype, calculate the model
    for genotype_id, genotype_vals in genotypes.items():

        # 2. Load Phenotypes 
        phenotype = load_phenotype(genotype_id, config["PHENOTYPES_DIR"])
        
        # Run the model for this specific phenotype
        result_score, result_phenotype = run(genotype_vals, phenotype)

        if LOG:
            print(f'[MODEL_RESULT]: Genotype_id: {genotype_id} Score: {result_score}, Phenotype: {result_phenotype}')

        # Save results
        res = {}
        res[genotype_id] = {"score": result_score, **result_phenotype}
        export_results(genotype_id=genotype_id, values=res, output_dir=config["OUTPUT_DIR"])
        
if __name__ == "__main__":
    try:
        config = load_config(CONFIG_FILE)
        main(config)
    except Exception as e:
        raise e