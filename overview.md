# Zeta Constraint Lab — Overview

This repository develops and validates a **symbolic governing field** for residual-flow systems using structured interaction bases.

## Core Idea

Instead of raw polynomial fitting or black-box ML, we construct a **minimal symbolic law**:

- preserves coupling between variables
- reduces redundant polynomial alignment
- generalizes across regimes

Final form:

g(c, r) =
β₀ + βc·c + βr·r + βrc·(r·c)
+ βc³·(c³ − αc)
+ βr²·(r² − β)
+ βrc²·(r·c²)

## Notebook Pipeline

### Foundation

- 64 v2 — Final governing field synthesis
- 65 v2 — Robustness validation (shuffle / ablation)
- 66 v2 — Constrained ML comparison

### Basis Selection

- 70 — Structured interaction vs alternatives

### Explanation (Why it works)

- 71 — Basis geometry + coupling analysis

### Final Extraction

- 72 — Paper-ready outputs

## Key Result

The structured_interaction basis achieves:

- low collinearity
- strong coupling retention
- high regime separation
- minimal term count

## Conclusion

A minimal symbolic law with structured coupling can match or exceed ML performance while remaining interpretable.
