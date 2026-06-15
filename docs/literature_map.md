# Literature Map

## Non-Smooth Contact Mechanics

Classical non-smooth dynamics and implicit time stepping already model unilateral contact, impact, and Coulomb friction. Complementarity formulations are a direct threat to any claim that the paper's residuals are novel.

## Robot Simulation and Contact Learning

MuJoCo and contact-learning methods already expose or learn contact transitions. This paper must avoid pretending that contact discontinuities are newly discovered.

## Foundation and Visuomotor Policies

Diffusion Policy, RT-1, and RT-2 demonstrate strong learned policy families. The paper's baselines are local surrogates, so the manuscript must not claim dominance over those systems as trained artifacts.

## Narrow Contribution

The defensible contribution is an executable audit: detect non-smooth contact-mode boundaries, reject invalid smooth extrapolations, and gate actions near impact, stick-slip, jam, and release regimes.
