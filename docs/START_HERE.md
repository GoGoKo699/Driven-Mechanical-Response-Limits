# Why reciprocal springs can have a nonreciprocal driven response

[Home](../README.md) · [Model](MODEL.md) · [Results](RESULTS.md)

## Two experiments, not one sideways motion

Imagine two accessible sliders. First apply a constant force to slider 1 and measure the displacement of slider 2. Then exchange the force and measurement locations. In an ordinary static linear spring system, the exchanged responses agree because the stiffness matrix, and hence its inverse, is symmetric.

A sideways displacement alone is not a sign of nonreciprocity. Static anisotropic springs can produce it. The relevant observable is the **difference between exchanged cross-responses**.

Now vary the spring stiffnesses according to a fixed repeating schedule. Do not measure the displacement to decide which force to apply next. Every instantaneous spring still derives from an elastic energy. Nevertheless, displacement evolves while the coefficients change. The order of configurations can then affect the measured response.

These statements concern the model developed here. Time-modulated mechanics and nonreciprocity have substantial predecessors; the [source guide](SOURCES.md) explains which ingredients are inherited.

## Keep the moving parts in the accounting

An early example is an anisotropic two-coordinate trap whose principal axes rotate. Its mean response can contain an antisymmetric part, but the measured object moves within every cycle. Attaching a spring changes that motion; one cannot generally add the load after replacing the device by its mean inverse compliance.

The attaining construction in this repository separates the roles. Two coordinates are measured and two are internal. Under a constant force, the measured pair settles to a constant displacement. The internal pair keeps cycling. The zero-frequency response therefore composes correctly with a static spring attached to the measured coordinates.

The internal motion dissipates energy against drag. The apparatus modulating the stiffness supplies that energy. Stationary measured outputs are not evidence of equilibrium or of an unpowered device.

## What is being optimized?

All compliant coordinates are counted, not just the observed ones. At every time, all stiffness eigenvalues must remain in the same interval $[m,M]$. Coordinates and their conjugate forces are fixed; a rescaling or lever that changes the normalized stiffness is not a free improvement.

The question is how large the absolute antisymmetric compliance can become, over all periods, schedules, and finite numbers of internal coordinates. The [ceiling](RESULTS.md#spectral-ceiling) answers it. Four coordinates attain it.

The number of coordinates alone is not the resource that explains an improvement over a planar device. Internal structure lets the same global spectrum allocate a different amount of stiffness to the measured directions. Fix that measured allocation as well, and the earlier planar ceiling survives even with more coordinates.

## What makes the proof short?

Represent the two real force experiments by one complex bookkeeping vector. Over a period, one balance describes the constant applied force; another describes the positive elastic quadratic form. In the inner product weighted by the instantaneous stiffness, a projection inequality bounds the response. A scalar bound on the inverse stiffness then removes the details of the waveform and internal dimension.

Complex numbers here combine two spatial experiments. Their imaginary part is not a phase lag under an oscillating probe force. The actual probe force stays constant.

## Three useful checks on understanding

**Would a damper exert a nonzero average force on a periodic trajectory?** No: its force averages to zero. It can still change the mean response by changing the within-cycle motion.

**Does four being minimal mean three coordinates cannot be nonreciprocal?** No. For force compliance, the minimum concerns exact ceiling attainment with stationary measured outputs and block-diagonal damping. Separately, four coordinates are necessary for the full clamped-response ceiling without those extra conditions. A suboptimal three-coordinate force-response control is supplied.

**Do positive physical spring constants permit any matrix coupling between parallel sliders?** No. Ordinary positive difference springs on parallel guides impose a positivity restriction. The proposed perpendicular guides and diagonal attachments supply the required generalized signs without negative physical springs.

Continue with the [precise model](MODEL.md), then the [short proof](PROOF.md). No prior research project or particular textbook is a prerequisite for this repository.
