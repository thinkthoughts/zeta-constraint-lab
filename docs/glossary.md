# Glossary

## Standard Terms

- **Riemann zeta function ζ(s)**: A complex function central to number theory and analytic continuation, usually introduced by
  \[
  \zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^s}
  \quad \text{for } \Re(s)>1,
  \]
  and extended to other values of \(s\) except \(s=1\).

- **complex plane**: The plane with horizontal axis \(\Re(s)\) and vertical axis \(\Im(s)\), used to visualize complex values of \(s\).

- **critical strip**: The region
  \[
  0<\Re(s)<1.
  \]

- **critical line**: The vertical line
  \[
  \Re(s)=\frac12.
  \]

- **zero**: A point \(s\) where
  \[
  \zeta(s)=0.
  \]

- **nontrivial zero**: A zero in the critical strip.

- **trivial zero**: A zero at the negative even integers
  \[
  -2,-4,-6,\dots
  \]

- **zero spacing**: The difference between imaginary parts of neighboring nontrivial zeros.

- **local window**: A small region of the complex plane or a short interval in \(t\) used to study nearby behavior of \(\zeta(1/2+it)\).

- **perturbation**: A small change in position or parameter, such as replacing \(\Re(s)=1/2\) by \(\Re(s)=1/2+\varepsilon\).

---

## TPL Framework Terms

These terms are used as a structural layer on top of the standard mathematics above.

- **TPL**: Short for **Triplet Phase Lock**, the broader framework behind this repo family. In this repo, TPL is used as a way to describe local structure, neighboring relations, and constraint-respecting behavior around zeta zeros.

- **constraint**: A condition that defines or stabilizes structured behavior. In this repo, the critical line
  \[
  \Re(s)=\frac12
  \]
  is treated as the main constraint boundary for experiments.

- **local structure**: Behavior of \(\zeta(s)\) in a small neighborhood, especially around nearby zeros or along a short interval of the critical line.

- **triplet / local triplet**: A local three-part neighborhood, usually:
  - left neighbor
  - center point
  - right neighbor

  For zeros, this often means three consecutive ordinates:
  \[
  t_{n-1},\; t_n,\; t_{n+1}.
  \]

- **phase-lock**: A stable local relation among neighboring features. In this repo, that may refer to balanced spacing, repeated local patterns, or stable behavior under small perturbations.

---

## VC and IA

These are TPL terms that should be used carefully and always with standard mathematical language nearby.

- **VC (Valid Construction)**: A structure, interpretation, or numerical setup that respects the governing constraint of the experiment.

  In this repo, examples of VC include:
  - evaluating \(\zeta(s)\) directly on the critical line
  - analyzing neighboring zero spacings using actual zero data
  - comparing perturbations against a clearly defined critical-line baseline

  VC does **not** mean “proof.”  
  It means the construction is internally consistent with the stated mathematical object and experiment.

- **IA (Invalid Assignment)**: A structure, interpretation, or labeling that imposes a conclusion without respecting the governing constraint.

  In this repo, examples of IA include:
  - treating an arbitrary off-line perturbation as equivalent to critical-line behavior without testing it
  - assigning structural meaning to noise or random placement without a defined comparison baseline
  - claiming that a numerical pattern is a theorem when it is only a heuristic observation

  IA does **not** mean “useless.”  
  It means the assignment is not yet justified by the stated structure or experiment.

---

## Repo-Specific VC / IA Interpretation

For **Zeta Constraint Lab**, the most useful practical reading is:

- **VC**
  - start from standard zeta definitions
  - define the constraint clearly
  - compute reproducibly
  - compare like with like
  - separate observed pattern from proven statement

- **IA**
  - skip definitions
  - blur critical-line and off-line behavior
  - treat visual resemblance as proof
  - mix exploratory language with theorem-level claims

---

## Working Translation Layer

This repo uses the following simple translation:

| Standard math term | TPL / repo term |
|---|---|
| critical line | constraint boundary |
| neighboring zeros | local triplet |
| zero spacing | local relation |
| stable repeated behavior | phase-lock |
| well-defined numerical experiment | VC |
| unjustified interpretation | IA |

---

## Usage Note

This glossary is meant to support exploration, not replace standard mathematics.

When possible, notebook text should follow this order:

1. standard mathematical term  
2. numerical observation  
3. optional TPL interpretation  

That keeps the repo readable to mathematicians, physicists, and general technical readers.
