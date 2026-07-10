import csv
import os

LOG = True

def validate_genotype_row(row):
    """
        Due to time limit and exercise intent, I'm only validating if it's not empty and it's a valid flat

    """
    if not row or len(row) < 5: # should have 5 columns (genotype_id, SNP1, SNP2, SNP3, SNP4) 
        return False
    if row[0] == '':
        return False
    for value in row[1:5]:
        if value == '':
            return False
        try:
            float(value)
        except ValueError:
            return False
    return True


def load_genotypes(GENO_FILE):
    """"
        
    """
    g = {}
    with open(GENO_FILE) as f:
        rows = csv.reader(f)
        next(rows)
        for r in rows:
            # genotype_id, SNP1, SNP2, SNP3, SNP4
            if not validate_genotype_row(r):
                continue
            g[r[0]] = [float(r[1]), float(r[2]), float(r[3]), float(r[4])]
    return g



def validate_phenotype_row(row):
    """
        Test function to validate phenotypes csv and assure columns are valid to run this program
    """
    if row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '':
        return False
    try:
        float(row[4])
    except (ValueError, TypeError):
        return False
    return True


def load_phenotype(genotype, phenotype_dir):

    phenotype_file = f'{phenotype_dir}{genotype}.csv'

    if LOG:
        print(f"[LOAD_PHENOTYPE] - Reading Phenotype file: ", phenotype_file)

    phenotypes = {}
    with open(phenotype_file, "r") as f:
        rows = csv.reader(f)
        next(rows)
        for r in rows:
            # genotype_id, SNP1, SNP2, SNP3, SNP4
            if not validate_phenotype_row(r):
                if LOG:
                    print(f'[LOAD_PHENOTYPE] - Invalid entry for Phenotype file: {phenotype_file} - {r}')
                continue
            trait = r[3]
            value = float(r[4])
            if trait not in phenotypes:
                phenotypes[trait] = []
            phenotypes[trait].append(value)
           
    return phenotypes


def export_results(genotype_id, values, output_dir):
    """
        values format {"score": float, trait: value}
    """

    for genotype_id, values in values.items():
        header_names = ["genotype_id"] + list(values.keys())
        out_path = os.path.join(output_dir, f"{genotype_id}.csv")

        with open(out_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=header_names)
            writer.writeheader()
            row = {"genotype_id": genotype_id}
            row.update(values)
            writer.writerow(row)