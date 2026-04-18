# Zeta Constraint Lab

Constraint-based exploration of ζ(s), zeros, and critical-line behavior.

---

## Overview

Zeta Constraint Lab is a small, reproducible project exploring the Riemann zeta function and its zero structure through numerical experiments.

Focus areas:
- evaluating ζ(s) across the complex plane  
- visualizing the critical line Re(s)=1/2  
- exploring zero spacing and local structure  
- testing simple constraint-style diagnostics  

This project does not claim a proof of the Riemann Hypothesis.  
Instead, it builds transparent experiments to better understand its structure.

---

## Quick Start

Open the first notebook in Google Colab:

👉 https://colab.research.google.com/github/thinkthoughts/zeta-constraint-lab/blob/main/notebooks/00_zeta_basics.ipynb

---

## Structure

```
zeta-constraint-lab/
├── notebooks/        # reproducible experiments
├── docs/             # glossary and notes
├── requirements.txt  # minimal dependencies
└── README.md
```

---

## Requirements

- Python 3.x  
- mpmath  
- numpy  
- matplotlib  

Install locally:

```
pip install -r requirements.txt
```

---

## Roadmap

- [ ] ζ(s) visualization (complex plane heatmaps)  
- [ ] critical-line sampling  
- [ ] zero spacing analysis  
- [ ] local constraint diagnostics  
- [ ] comparison with randomized controls  

---

## Context

This repo is part of a broader constraint-based framework applied across:
- number theory  
- computational complexity  
- quantum systems  

---

## License

MIT
