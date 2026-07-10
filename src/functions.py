import csv
import os

def load_genotypes(GENO_FILE):
    """"
        
    """
    g = {}
    with open(GENO_FILE) as f:
        rows = csv.reader(f)
        next(rows)
        for r in rows:
            # genotype_id, SNP1, SNP2, SNP3, SNP4
            g[r[0]] = [float(r[1]), float(r[2]), float(r[3]), float(r[4])]
    return g



def validate_phenotype_row(row):
    """
        Test function to validate phenotypes csv and assure columns are valid to run this program
    """
    if row[0] == '' or row[1] == '' or row[2] == '':
        return False
    try:
        float(row[3])
    except (ValueError, TypeError):
        return False
    return True