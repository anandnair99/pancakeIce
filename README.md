# pancakeIce
Pancake ice and wave interaction CFD model made in OpenFOAM.

# Overview
- Floating body and wave interaction model using the overset mesh method and VOF interface capturing.
- `sixDoFRigidBodyMotion` library and `interFoam` series solver, `overInterDyMFoam`.
- `StokesI` and `StokesII` wave models tested.
- Created on v2112. Tested on v2106, v2112, v2306 and v2312.

![pancakeIceDisk mp4_snapshot_00 32_ 2022 12 14_15 05 18](https://github.com/user-attachments/assets/62dc5c6e-2439-4660-89dd-abd01f46dbec)
*Pancake ice model v1*
![MeshBocks_long mp4_snapshot_00 07 461](https://github.com/user-attachments/assets/5278e3ad-7cf4-417b-8aeb-a2905e2bbc2d)
*Pancake ice model v2*

Improvements
- Refinement zone added to free surface region to improve free surface capturing
- Grid size refined.
- Parameters tuned to match MIZ observations in model scale

# License
This project is licensed under the MIT license.
