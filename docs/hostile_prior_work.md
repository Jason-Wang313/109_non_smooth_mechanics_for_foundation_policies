# Hostile Prior Work

The broad claim "robot policies need contact mechanics" is crowded and should not be made.

Relevant pressure points:
- Moreau's non-smooth contact dynamics formalizes unilateral contact and impacts.
- Stewart and Trinkle-style implicit time stepping handles rigid-body contact with friction.
- Anitescu and Potra connect multi-rigid-body contact with friction to complementarity formulations.
- MuJoCo and related simulators already expose contact-aware dynamics for robot learning.
- ContactNets and related work learn discontinuous contact dynamics.
- Diffusion Policy, RT-1, and RT-2 show that learned visuomotor or vision-language-action policies can solve many manipulation tasks without this paper's proposed atlas.

The novelty boundary is therefore narrow: this paper is not a new contact solver or a generic foundation-model claim. It is a local evidence claim that contact-mode boundary auditing helps prevent smooth policy interpolation across non-smooth mechanics events.
