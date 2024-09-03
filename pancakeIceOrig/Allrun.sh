#!/bin/sh

#SBATCH --account=eleceng
#SBATCH --partition=ada
#SBATCH --nodes=1 --ntasks=40
#SBATCH --time=10:00:00
#SBATCH --job-name="pancakeIce"
#SBATCH --mail-user=nrxana001@myuct.ac.za
#SBATCH --mail-type=BEGIN,END,FAIL

# OpenFOAM
SINGULARITY_PATH=/opt/exp_soft/singularity-containers
FOAM_BASHRC=/opt/OpenFOAM/OpenFOAM-v2106/etc/bashrc

cd floatingBody
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif blockMesh
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif snappyHexMesh -overwrite
cd ../background
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif blockMesh
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif mergeMeshes . ../floatingBody -overwrite
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif topoSet
cp -r 0.orig 0
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif setFields
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif decomposePar
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif mpirun -np 8 overInterDyMFoam -parallel
singularity exec $SINGULARITY_PATH/openfoam/openfoam-v2106.sif reconstructPar

rm -r processor*
cd ..
cd ..
zip -r pancakeIce.zip pancakeIce