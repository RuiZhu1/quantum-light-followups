# Learning guide and instruction contract

## Purpose

This is a graduate-level implementation project, not a finished software package. The goal is to learn the derivations, numerical methods, detector physics, and scientific judgment needed to complete Projects A and B. The project note and the skeleton comments are starting guidance, not an answer key.

The code is intentionally incomplete. Functions marked with `NotImplementedError` must be implemented and explained by the student.

## Instruction labels

| Label | Status | What the student may change |
|---|---|---|
| `REQUIRED` | A mathematical, physical, reproducibility, or process constraint that must be satisfied. | Only the implementation, provided the constraint remains satisfied and is tested. Do not relax the constraint merely to obtain agreement with the project note. |
| `GUIDED` | A recommended derivation or implementation route. | A different route is allowed if it is justified, validated, and documented. |
| `OPEN` | An intentionally open design or research choice. | Choose or design an approach. There is no preferred hidden implementation. |
| `THINK` | A conceptual question requiring a written answer in the student's own words. | Do not answer by copying code or generated prose. Use the derivation and literature. |
| `CHALLENGE` | An optional opportunity to improve the original design or claim. | Proceed only after the required version works. A stronger claim needs a proof or stronger validation. |

The instructions themselves are not guaranteed to be optimal or immune to error. If a conflict appears, preserve evidence, identify the incorrect assumption, and discuss it at the milestone meeting instead of silently following the instruction.

## Strict process rules

1. Read the relevant part of `quantum_light_followups.pdf` and the listed papers before implementing a milestone.
2. Derive the governing equations independently before coding them. The PDF's numerical values are targets to investigate, never constants to hard-code into a solver.
3. Every probability model must pass positivity, normalization, Born-rule, and relevant limiting-case checks.
4. Every numerical result must include its parameters, convergence evidence, and an independent or limiting-case check where possible.
5. Clearly separate analytical results, numerical observations, Monte Carlo simulations, and laboratory measurements.
6. Use AI only in small, reviewable steps. Record what was suggested, what was accepted or rejected, and what was independently verified. The student must be able to explain every derivation and every line of submitted code.
7. Do not generate an entire project, paper, or proof in one step. Do not use generated agreement with a target number as a substitute for understanding.
8. Meet Marcelo after every milestone. Present the derivation, implementation, tests, figures, assumptions, and unresolved questions. Start the next milestone only after that discussion and the required corrections.
9. A better design is welcome, but it must be documented as a deliberate alternative rather than an accidental departure from the instructions.

## Milestone meeting package

Prepare the following before each meeting:

- A short derivation or literature note in the student's own words.
- The specific skeleton functions completed during the milestone.
- Test output and convergence or limiting-case checks.
- Figures with parameters and uncertainty information where applicable.
- A short AI-use and verification log.
- A list of disagreements, failed attempts, assumptions, and open questions.
- A clear decision on whether the milestone is complete or needs another iteration.

## What completion means

A milestone is not complete merely because code runs or a plot resembles the project note. It is complete when the student can explain why the model is appropriate, why the implementation is correct, what its limitations are, and what evidence supports each claim.
