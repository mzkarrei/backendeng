

import csv
import glob
import os
 

GENOTYPE_FILE = "data/genotypes/markers.csv"
PHENOTYPE_DIR = "data/phenotypes/"

OUTPUT_DIR = "data/phenotypes_prod/"

LOG = True

def load_genotype_ids(geno_file=GENOTYPE_FILE):
    ids = []
    with open(geno_file, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ids.append(row["genotype_id"])
    return ids

def create_phenotype_empty_file(geno_id, output_path=OUTPUT_DIR):

    if LOG:
        print(f'[NEW PHENOTYPE FILE] - Creating phenotype file for genotype: {geno_id}')

    output_file = f'{output_path}/{geno_id}.csv'
    with open(output_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["plot_id", "site", "genotype_id", "trait", "value"])
        writer.writeheader()

def main():

    unique_rows = set() # Avoid duplicates


    genotype_ids = load_genotype_ids(GENOTYPE_FILE)

    for id in genotype_ids:
        create_phenotype_empty_file(id)

    phenotype_files = glob.glob(os.path.join(PHENOTYPE_DIR, "*.csv"))

    for filepath in phenotype_files:
        site = os.path.splitext(os.path.basename(filepath))[0]

        with open(filepath, newline="") as f:
            if LOG:
                print(f'[READING SITE PHENOTYPE] - Reading original phenotype file from site: {site}')

            reader = csv.reader(f)
            next(reader)
            for row in reader:
                plot_id, genotype_id, trait, value = row[0], row[1], row[2], row[3]

                # Check duplicates
                key = (plot_id, site, genotype_id, trait, value,)
                if key in unique_rows:
                    if LOG:
                        print(f'SKIPPING DUPLICATED PHENOTYPE')
                    continue
                unique_rows.add(key)
                
                phenotype_prod_file = f'{OUTPUT_DIR}/{genotype_id}.csv'
                
                with open(phenotype_prod_file, "a", newline="") as out_f:
                    writer = csv.DictWriter(out_f, fieldnames=["plot_id", "site", "genotype_id", "trait", "value"])
                    writer.writerow({
                        "plot_id": plot_id,
                        "site": site,
                        "genotype_id": genotype_id,
                        "trait": trait,
                        "value": value
                    })


if __name__ == '__main__':
    main()