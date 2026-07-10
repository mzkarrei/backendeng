#!/usr/bin/env python
# quick script to crunch the trial data - Dr. Reyes
# run it like: python analyze_trials.py
# (you might have to change the folder path below)

import os
import csv
import statistics

DATA_DIR = "data/phenotypes"
GENO_FILE = "data/genotypes/markers.csv"
OUT = "results.csv"

# marker weights we settled on last season (don't change these)
W = {"SNP1": 0.4, "SNP2": 0.1, "SNP3": 0.35, "SNP4": 0.15}


def load_genotypes():
    g = {}
    f = open(GENO_FILE)
    rows = csv.reader(f)
    next(rows)
    for r in rows:
        # genotype_id, SNP1, SNP2, SNP3, SNP4
        g[r[0]] = [float(r[1]), float(r[2]), float(r[3]), float(r[4])]
    return g


def score(markers):
    # genomic estimated value - weighted sum
    # NOTE: this Python version is slow on the full marker panel. Priya rewrote it
    # in C++ (see scoring.cpp) - we should be using that instead, it just isn't
    # hooked up yet.
    return markers[0]*W["SNP1"] + markers[1]*W["SNP2"] + markers[2]*W["SNP3"] + markers[3]*W["SNP4"]

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

def main():
    genos = load_genotypes()

    # read every phenotype file into memory
    all_rows = []
    files = os.listdir(DATA_DIR)
    for fn in files:
        f = open(DATA_DIR + "/" + fn)
        rows = csv.reader(f)
        next(rows)
        for r in rows:
            all_rows.append(r)

    # group measurements by genotype
    by_geno = {}
    for r in all_rows:
        # plot_id, genotype_id, trait, value

        if not validate_phenotype_row(r): # Skip invalid row
            continue

        gid = r[1]
        if gid not in by_geno:
            by_geno[gid] = {}
        trait = r[2]
        if trait not in by_geno[gid]:
            by_geno[gid][trait] = []
        by_geno[gid][trait].append(float(r[3]))

    # compute per-genotype summary + genomic score
    results = []
    for gid in by_geno:
        yield_vals = by_geno[gid]["yield"]
        height_vals = by_geno[gid]["height"]
        gval = score(genos[gid])
        results.append([
            gid,
            statistics.mean(yield_vals),
            statistics.mean(height_vals),
            gval,
        ])

    # sort by genomic score, best first
    results.sort(key=lambda x: x[3], reverse=True)

    out = open(OUT, "w")
    out.write("genotype_id,mean_yield,mean_height,genomic_score\n")
    for row in results:
        out.write(str(row[0]) + "," + str(row[1]) + "," + str(row[2]) + "," + str(row[3]) + "\n")

    print("done, wrote " + str(len(results)) + " genotypes")

if __name__ == "__main__":
    main()
try:
    main()
except:
    pass
