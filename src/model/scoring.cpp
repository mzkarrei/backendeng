// scoring.cpp
//
// Faster genomic-score routine. Matt wrote this in C++ because the
// Python version was too slow when we tried it on the full marker panel last
// month. It's not wired into the pipeline yet -- someone just needs to hook it up.
//
// The math must match the current Python score() exactly (same marker weights),
// otherwise the rankings change and the breeders will (rightly) complain.
//
// Quick sanity check:
//   genomic_score(0.82, 0.10, 0.55, 0.31) == 0.577   (SNP1..SNP4 for G001)
//
// Build notes: this is just the raw function. It compiles with any C++11
// compiler. It is currently standalone -- there is no Python binding yet.

// Marker weights we settled on last season. DO NOT change these numbers.
static const double W_SNP1 = 0.40;
static const double W_SNP2 = 0.10;
static const double W_SNP3 = 0.35;
static const double W_SNP4 = 0.15;

// Genomic estimated value: weighted sum of the four SNP marker dosages for a
// single genotype.
double genomic_score(double snp1, double snp2, double snp3, double snp4) {
    return snp1 * W_SNP1 + snp2 * W_SNP2 + snp3 * W_SNP3 + snp4 * W_SNP4;
}
