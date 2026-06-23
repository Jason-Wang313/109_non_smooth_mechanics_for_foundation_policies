# Experiment Rigor Checklist

- [x] Frozen v5 execution plan written before final edits and experiments.
- [x] Paired seeds across methods.
- [x] Strong non-oracle baselines: v4 atlas, robust hybrid MPC, complementarity residual planner, contact-implicit MPC, conformal risk filter, ensemble disagreement, diffusion-policy surrogate, robotics-transformer surrogate, smooth world model, learned contact classifier, energy barrier policy, domain randomization, and no-contact BC.
- [x] Oracle references retained to expose headroom.
- [x] Eight contact-rich task families.
- [x] Ten non-smooth regimes including impact, stick-slip, unilateral lift-off, jamming, release snap, compliance shift, friction-cone inversion, actuator backlash, and mixed shock.
- [x] Eight deployment splits including unseen geometry, friction, compliance, actuator latency, sensor dropout, and held-out mixed stress.
- [x] Safety metrics reported alongside success and utility.
- [x] Pairwise seed statistics emitted.
- [x] Component ablations remove coupled arbitration when required channels are removed.
- [x] Stress sweep emitted.
- [x] Fixed-risk acceptance emitted.
- [x] Twenty-four failure cases documented.
- [x] Validator checks row counts, gates, finite numeric values, PDF properties, and artifact location.
- [ ] Real robot validation.
- [ ] Independent high-fidelity simulator validation.
- [ ] External trained policy checkpoints.
