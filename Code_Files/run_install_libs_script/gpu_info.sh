#!/bin/bash
#SBATCH --job-name=gpuinfo
#SBATCH --output=logs/gpuinfo.out.%j
#SBATCH --error=logs/gpuinfo.err.%j
#SBATCH -N 1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=1
#SBATCH --time=00:05:00

echo "Partition: $SLURM_JOB_PARTITION"
echo "Host: $(hostname)"
echo
echo "===== CPU INFO ====="
lscpu
echo
echo "===== GPU INFO ====="
nvidia-smi

# Example submissions:
# sbatch -p gpua gpu_info.sh
# sbatch -p gpub gpu_info.sh
# sbatch -p gpuc gpu_info.sh