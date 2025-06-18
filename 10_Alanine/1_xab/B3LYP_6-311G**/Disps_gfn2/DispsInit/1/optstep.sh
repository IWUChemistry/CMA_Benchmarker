#!/bin/bash
#SBATCH --job-name=Concordant             # Job name
#SBATCH --partition=batch               # Partition (queue) name
#SBATCH --cpus-per-task=4     # Number of cores per MPI rank 
#SBATCH --mem=40GB        # Memory per processor
#SBATCH --time=72:00:00
#SBATCH --output=output.dat
#SBATCH --hint=compute_bound

source /nfs/cluster_config/modules.sh
module load xtb/6.7.1

#eval "$(conda shell.bash hook)"
## Load their personal Conda environment
#conda activate xtbenv
#capture the submission directory
SUBMIT_DIR="$SLURM_SUBMIT_DIR"

#scratch directory
SCRATCH_DIR="/scratch/$USER/$SLURM_JOB_ID"

srun --cpu-bind=verbose xtb --gfn 2 input.coord --hess --grad


echo "Job \$SLURM_JOB_ID running on \$HOSTNAME"
echo "CPU affinity:"
taskset -cp $$
