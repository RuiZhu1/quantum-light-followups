# Milestones, reading, and meeting gates

Read `LEARNING_GUIDE.md` before starting. The order is intentional. Each milestone ends with a meeting with Marcelo; do not begin the next milestone until the current one has been discussed and corrected where necessary.

The project note contains proposed results, not pre-approved answers. Reproduce them only after deriving the model and implementing the calculation.

## 1. Baseline, literature, and reproducibility

### Purpose

Understand the majorization protocol and establish a clean baseline before developing either project.

### Read first

- `quantum_light_followups.pdf`: abstract, Sec. 1, and the shared toolkit in Sec. 4.
- `paper/main.pdf`: the definitions, projective bounds, POVM bound, attainment, detector proposition, steering corollary, and numerical appendix.
- Friedland, Gheorghiu & Gour (2013), **Universal Uncertainty Relations**.
- Puchała, Rudnicki & Życzkowski (2013), **Majorization entropic uncertainty relations**.
- Rudnicki, Puchała & Życzkowski (2014), **Strong majorization entropic uncertainty relations**.
- Baek, Nha & Son (2019), for the POVM partial-sum eigenvalue formula.
- Li & Qiao (2019), for optimality and saturating states.
- Coles et al. (2017), as optional review background.

### Implement or inspect

- Read every task in `code/majorization.py` and `code/verify_bounds.py` before implementing anything.
- Set up the environment and record Python, NumPy, SciPy, and Matplotlib versions.
- Write a plan for independently testing Lorenz curves, majorization, and entropy functions.

### Deliverable

A short note explaining direct sum versus tensor product, majorization-lattice optimality versus entropy-specific optimality, and why a lattice supremum need not be a state's statistics. Include a baseline test plan and a reference list.

### Think and discuss

- What does one majorization vector buy that a single Shannon inequality does not?
- Which claims in the project note are analytical, numerical, or experimental?
- What evidence would be needed before trusting a new numerical result?

**Meeting gate:** review the note and test plan with Marcelo.

## 2. Project A: single-photon detector model

### Purpose

Derive the POVM of the polarization analyzer actually used, including detector imperfections and click assignment.

### Read first

- Project note: Sec. 2.1 and Sec. 2.2 through Eq. (9).
- Busch (1986), for unsharp spin measurements.
- Makarov, Anisimov & Skaar (2006), for efficiency mismatch.
- Beaudry, Moroder & Lütkenhaus (2008), for detector squashing and its limitations.
- Klyshko (1980), as optional detector-calibration background.

### Implement

Complete the single-photon detector tasks in `code/project_a.py`. Start from the effects, not from the final bias formula. Validate positivity, normalization, Born-rule probabilities, and the no-dark-count limit.

### Deliverable

A derivation of the single-photon effects, the implementation, and tests for equal efficiencies, extreme efficiencies, zero dark counts, and alternative click-assignment rules.

### Think and discuss

- Which assumptions make the model diagonal in the H/V basis?
- What changes if double clicks are assigned deterministically rather than randomly?
- Which parts are detector physics and which are merely outcome post-processing?

**Meeting gate:** review the derivation and tests with Marcelo before using the model in Fock space.

## 3. Project A: Fock-space and multi-photon model

### Purpose

Construct binary measurements for multi-photon inputs and determine when a single-photon bound is unsafe.

### Read first

- Project note: Eq. (10), Eq. (11), Table 1, and the multi-photon discussion.
- Baek, Nha & Son (2019), for the eigenvalue construction.
- Yuan et al. (2023), for optimal direct-sum bounds and experimental context.
- Beaudry, Moroder & Lütkenhaus (2008), for the connection to squashing.
- Halmos (1969), as optional projector background.

### Implement

Complete the Fock-effect and partial-sum tasks in `code/project_a.py`. Use the general operator solver in `code/majorization.py` only after implementing and testing it. Include rotations and truncation-convergence checks.

### Deliverable

A multi-photon bound calculation, convergence evidence, and an explanation of why the tighter single-photon vector can fail. Compare the one-photon and Fock-space results without hard-coding the project note's table.

### Think and discuss

- Is a post-selected single-photon model equivalent to keeping all click outcomes?
- What determines a safe bound for an unknown photon-number distribution?
- Can a better truncation or block structure reduce the computation?

**Meeting gate:** discuss the convergence and the physical meaning of the correction with Marcelo.

## 4. Project A: Monte Carlo virtual experiment

### Purpose

Mimic the counting experiment and test the full analysis pipeline before using real or simulated data for physical claims.

### Read first

- Project note: Secs. 2.3–2.6 and Table 2.
- James et al. (2001), for maximum-likelihood reconstruction.
- Klyshko (1980), for calibration context.
- Efron (1979), **Bootstrap Methods: Another Look at the Jackknife**, as optional statistical background.
- Makarov et al. (2006), for efficiency-mismatch systematics.

### Implement

Complete the Monte Carlo tasks in `code/project_a.py`. Simulate counts from the model, not from precomputed plots. Include counting noise, calibration uncertainty, bootstrap intervals, and systematic variations.

### Deliverable

Synthetic data, analysis output, and a comparison between sampled and analytic probabilities. Include an error budget and an explanation of statistical versus systematic uncertainty.

### Think and discuss

- Can the pipeline recover the non-attainment gap without using the answer as an input?
- Which systematic error dominates at the chosen angle?
- What sampling or estimation design could improve the experiment?

**Meeting gate:** review the virtual experiment with Marcelo and decide whether it is ready for steering or laboratory data.

## 5. Project A: Lorenz gap, detector maps, and steering

### Purpose

Connect the calibrated measurement model to attainment, detector-bias failure, and false steering certification.

### Read first

- Project note: the steering model, WP-A3/WP-A4, and expected results.
- Walborn et al. (2011), Schneeloch et al. (2013), and Uola et al. (2020), for entropic steering.
- Saunders et al. (2010), for one-sided photonic steering.
- Skrzypczyk & Cavalcanti (2015), for loss-tolerant steering.
- Rutkowski et al. (2017), for measurement-setting-error tolerance.

### Implement

Complete the Lorenz-gap and steering tasks in `code/project_a.py`. Include a product-state example, Bell/Werner scans, and both the exact-Shannon and majorization bounds. Do not treat either witness threshold as a fundamental steering boundary.

### Deliverable

A virtual or laboratory analysis chain showing the false violation under the ideal bound and its removal under the appropriate actual-POVM analysis. Include Lorenz curves, a gap estimate, mismatch maps, and steering scans.

### Think and discuss

- What distinguishes a violated ideal bound, a violated actual LHS inequality, and a false experimental certification?
- Which calibration assumptions are essential to the correction?
- What can the majorization witness offer despite its weaker Shannon threshold?

**Meeting gate:** present the full Project A story and limitations to Marcelo.

## 6. Project B: binned quadratures and the Zak/GKP reduction

### Purpose

Derive a nontrivial binary measurement on a light mode and establish the exact qubit reduction at period product `4 pi`.

### Read first

- Project note: Secs. 3.1–3.2 through Eq. (15).
- Zak (1967) and Aharonov, Pendleton & Petersen (1969), for modular variables and the Zak transform.
- Gottesman, Kitaev & Preskill (2001), for the GKP setting.
- Pantaleoni, Baragiola & Menicucci (2020), for the modular subsystem decomposition.
- Halmos (1969) and Kaniewski, Tomamichel & Wehner (2014), for projector/block tools.

### Implement

Complete the clock/shift and block-projector tasks in `code/project_b.py`. First test small finite matrices, then connect them to the binned projectors. Derive the `r = 1/2` case analytically before numerical exploration.

### Deliverable

An independent derivation and small-matrix checks of the Weyl relation, block action, and the claimed Pauli-Z/Pauli-X reduction.

### Think and discuss

- Why does an odd-dimensional block force a common eigenvector?
- What is the logical interpretation of eigenstate and bisector states in the GKP mapping?
- Where could the finite-block argument fail for a physical finite-energy state?

**Meeting gate:** review the derivation with Marcelo before computing `c(r)` numerically.

## 7. Project B: overlap map and energy-constrained overlap

### Purpose

Compute the overlap on rational blocks and formulate a physically meaningful finite-energy version.

### Read first

- Revisit the Zak, GKP, and modular-subsystem references from Milestone 6.
- Rudnicki, Walborn & Toscano (2012), for coarse-grained entropic uncertainty.
- Tasca et al. (2013), for coarse-grained photonic measurements.
- Search for additional energy-constrained optimization literature as needed; record the search rather than assuming the project note covers it.

### Implement

Complete the block-overlap and energy-constraint tasks in `code/project_b.py`. Report block-size, grid, and truncation convergence. Treat irrational or infinite-energy behavior as open unless independently established.

### Deliverable

A reproducible `c(r)` calculation and a documented formulation of `c_E(r)`, including limitations and convergence tests.

### Think and discuss

- Why can `c(r)` be discontinuous?
- Is `c_E(r)` a property of a measurement alone or of a measurement plus an energy constraint?
- Which optimizer or representation is most reliable, and can you design a better one?

**Meeting gate:** discuss both the map and the limits of the numerical evidence with Marcelo.

## 8. Project B: loss, binning bias, and optical applications

### Purpose

Apply the binary theory to realistic homodyne detection and optical states, and determine what the resulting witnesses can and cannot show.

### Read first

- Project note: homodyne loss, duty-cycle errors, non-Gaussianity, EPR steering, and Tables 3–4.
- Lvovsky & Raymer (2009), for homodyne detection.
- Reid (1989), for the Reid steering criterion.
- Ourjoumtsev et al. (2007) and Lewenstein et al. (2021), for optical cats.
- Vahlbruch et al. (2016) and Eberle et al. (2013), for experimental squeezing context.
- Rudnicki et al. (2012) and Tasca et al. (2013), for coarse-grained witnesses.

### Implement

Complete the homodyne-loss, duty-cycle, state-evaluation, and steering tasks in `code/project_b.py`. Evaluate squeezed, cat, and GKP-type states. Treat the proposed Gaussian bound as a claim requiring proof or independent validation, not as an assumption.

### Deliverable

Tolerance maps and application figures, a non-Gaussianity analysis, and an EPR-steering comparison that includes the Reid criterion and the binary witness's limitations.

### Think and discuss

- Why is homodyne loss unsharpness while duty-cycle error can be bias?
- Can a better non-Gaussianity bound or state family be found?
- Why can a weaker binary witness still be useful?

**Meeting gate:** review each application separately with Marcelo before assembling Project B.

## 9. Independent review, reconstruction, and writing

### Purpose

Turn the completed milestones into defensible research outputs rather than a collection of generated plots.

### Read again

- The project note and the current manuscript.
- The papers that turned out to be essential in each milestone.
- `paper/revision_notes.md`, to understand the distinction between analytical results, numerical observations, and presentation decisions in the reference manuscript.

### Complete

- Re-derive the main equations without referring to the implementation.
- Regenerate every figure from the implemented models.
- Run all tests and document convergence, limitations, and failed approaches.
- Prepare separate thesis or paper outlines for Projects A and B.

### Deliverable

A clean, student-implemented package, a written derivation for each project, verified figures, and a list of what remains open. Include an AI-use log and a statement of which designs were changed deliberately and why.

### Final discussion with Marcelo

Review the scientific claims, the student's understanding, the limitations, and whether either project is ready for laboratory data, a partner group, or manuscript preparation. Do not treat the package as complete merely because all code runs.
