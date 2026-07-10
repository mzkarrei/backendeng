# Take-Home Exercise: Productionizing a Research Pipeline

Thanks for your interest in the AI Backend Engineer role. This exercise is meant to
reflect the actual work you'd do here: taking useful-but-rough analysis code
written by a scientist and turning it into something we can run reliably, at
scale, without a person watching it.

## Time expectation

**Please spend no more than 3–4 hours on this.** We are deliberately asking for
more than can be finished in that time. We are far more interested in *how you
prioritize and reason* than in a "complete" solution. A focused, well-documented
partial solution beats a rushed attempt at everything. Tell us what you chose
*not* to do and why — that's part of the signal.

## The situation

Dr. Reyes, a plant breeder, wrote `analyze_trials.py` to process field-trial
data. For each genotype it averages the phenotype measurements (yield, height)
collected across trial plots, combines them with a genomic marker score, and
ranks the genotypes. It runs on her laptop against one season's data.

We now want to run this kind of analysis routinely across **thousands of input
files** from many trial sites, on a schedule, as part of our data platform —
with no one manually re-running it or eyeballing the output. Right now it is not
close to ready for that.

The code is in this repo. A small sample dataset is under `data/`. Note the
script currently has hardcoded paths near the top that you'll need to point at
the sample data.

## Your task

Evolve `analyze_trials.py` into something you'd be comfortable putting into
production. You have full latitude on structure, libraries, and design. We
suggest working roughly in this order and stopping when your time is up:

### 1. Make it correct and robust (start here)
- Get it running against the sample data in `data/`.
- The sample data contains realistic problems. A single bad record or file
  should not take down the entire run. Decide what "handle it" means and do that.
- Preserve the analysis logic and the marker weights — the science shouldn't change.

### 2. Make it production-quality code
- Structure the code the way you'd want to maintain it.
- Add tests for the parts that matter most.
- Make failures visible and diagnosable (someone will get paged about this at
  2 a.m. — what do they need?).

### 3. Wire in the C++ scorer
A colleague on the team rewrote the genomic-scoring function in C++
(`scoring.cpp`) because the Python version is too slow on the full marker panel.
It compiles but isn't connected to anything yet.

- Integrate `genomic_score` from `scoring.cpp` so the pipeline uses it instead of
  the Python `score()`. Keep the numbers identical — the science must not change.
- Include how to build it and how you'd package/ship it.
- Efficiency at the Python↔C++ boundary matters: at scale we score a very large
  number of genotypes. Design the interface with that in mind.
- Add at least one test that exercises the boundary.

### 4. Make it ready to scale (in code)
- Sketch or implement how this processes thousands of files rather than three.
- Consider throughput, memory, restarts/re-runs, and partial failure.
- You do **not** need to build distributed infrastructure here. Implement what's
  reasonable in the time, and describe the rest.

### 5. Architect the production system on AWS (`ARCHITECTURE.md`) — design only, no code
This is the part we most want to see your systems thinking on. **Write and draw,
don't build.** We use AWS. Design the system that would run this analysis as a
managed, hands-off pipeline given the scenario below.

**The scenario, concretely:**
- ~12 trial sites upload phenotype files to us throughout the day. On a busy
  night that's on the order of **50,000 files**, from a few KB to several GB each.
- The pipeline runs **nightly** but should also pick up late-arriving files.
- Scoring a batch can take anywhere from **seconds to a couple of hours**
  depending on panel size.
- We must **not reprocess** a file we've already done, and must **safely resume**
  after a crash without double-counting.
- **Hundreds of scientists** later query the results interactively — filtering and
  joining across genotypes, traits, sites, and seasons — from an internal
  dashboard.
- When something breaks overnight, the on-call engineer needs to find out
  *without* a human having watched it.

**Please include:**
- **A diagram** of the architecture (ASCII, Mermaid, or a photo of a whiteboard
  is completely fine).
- **A component table** — for each AWS service you'd use, one line on *what role
  it plays* and *why you chose it over the obvious alternative.* We're specifically
  interested in your reasoning about: compute (e.g. Lambda vs. containers/Batch),
  a queue, where you keep **per-file processing state**, and where the
  **scientists' query data** lives. Name the services you'd actually use.
- **Trace one file** end to end: from landing in the system to a scientist seeing
  its results. What happens at each hop, and what happens if that hop fails?
- **Two judgment calls, explicitly:**
  - Where would you use a **key-value store (e.g. DynamoDB)** vs. a **relational
    database (e.g. RDS/Aurora)**, and why? What goes in each?
  - Where does a **serverless function (Lambda)** fit, and where would it be the
    *wrong* choice for this workload? Why?
- **Failure & scale:** what breaks first as volume grows 10×, how you'd know
  (metrics/alarms), and how poison/corrupt files are contained.

### 6. Write it up (`DESIGN.md`) — please don't skip this
A short document (roughly 1–2 pages) covering:
- **What you changed and why**, and what you deliberately left out.
- **The C++ integration:** how you bound it to Python, how data crosses the
  boundary, and how that holds up when scoring millions of genotypes.
- **Dependability:** What are the top ways this fails in production over a year
  of running, and what would you do about them?
- **If you had another day**, what would you do next?
- **(Optional, a few sentences — no implementation) Looking ahead with AI:** We
  expect to use LLMs and possibly agentic workflows to make this pipeline more
  useful to scientists. Where would you apply AI here, and — just as important —
  where would you deliberately *not*? We're interested in your instincts; there's
  no wrong answer, and skipping this won't count against you.

## What to hand back

A git repo (a zip is fine) containing:
- Your updated code, including the C++ binding
- Instructions to build the C++ extension and run everything
- Tests and instructions to run them
- `ARCHITECTURE.md` (with a diagram) and `DESIGN.md`

## How we'll evaluate

We care about: sound engineering judgment, code we'd want to maintain, realistic
handling of failure and scale, and clear communication of trade-offs. We do
**not** expect a finished production system, cloud deployment, or that you use
any specific framework. Working, well-reasoned, and honest about its limits beats
big and broken.

If anything is ambiguous, make a reasonable assumption, note it, and move on —
just like you would here.

Good luck, and thank you for your time.
