
import statistics

# marker weights we settled on last season (don't change these)
W = {"SNP1": 0.4, "SNP2": 0.1, "SNP3": 0.35, "SNP4": 0.15}


def score(markers):
    # genomic estimated value - weighted sum
    # NOTE: this Python version is slow on the full marker panel. Priya rewrote it
    # in C++ (see scoring.cpp) - we should be using that instead, it just isn't
    # hooked up yet.
    return markers[0]*W["SNP1"] + markers[1]*W["SNP2"] + markers[2]*W["SNP3"] + markers[3]*W["SNP4"]


def run(genotype_values, phenotype):
    """
        I'd standardize the initial model function name, in case we have any other starter file,
        such as a Lambda Function, local script, or any other script integration, it'd be easier to integrate
    """
    # Calculate phenotype summary 
    genotype_score = score(genotype_values)

    # Dynamically calculate mean for different phenotypes
    phenotype_means = {trait: statistics.mean(values) for trait, values in phenotype.items()}
    
    return genotype_score, phenotype_means