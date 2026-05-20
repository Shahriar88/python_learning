#!/bin/bash
#SBATCH -N 1
#SBATCH -n 1
#SBATCH -p gpu-h100
#SBATCH --mail-user=username@gmail.com
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --cpus-per-task=6
#SBATCH --time=2-00:00:00

# #SBATCH --gres=gpu:1
# ============================================================
# Copy files or folders from local computer to TACC
# ============================================================

# Copy a folder recursively:
# scp -r -o MACs=hmac-sha2-256 FOLDER username@ls6.tacc.utexas.edu:/work/number/user/ls6/shahriar/projects/Div2k/

# Copy one or more files:
# scp -o MACs=hmac-sha2-256 file1.py file2.sh username@ls6.tacc.utexas.edu:/work/number/user/ls6/shahriar/projects/Div2k/


# ============================================================
# Job submission examples
# ============================================================

# Example 1: Let Slurm choose an available node from the default partition specified above.
# This submits job1.py using the default partition in this script.
# export JOB=job1; mkdir -p logs; sbatch --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"

# Example 2: Submit to the gpu-a100-small partition and let Slurm choose the node.
# export JOB=job2; mkdir -p logs; sbatch -p gpu-a100-small --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"

# Example 3: Submit to the full gpu-a100 partition and let Slurm choose the node.
# export JOB=job3; mkdir -p logs; sbatch -p gpu-a100 --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"

# Example 4: Submit to the gpu-h100 partition and request a specific H100 node.
# export JOB=vit0; mkdir -p logs; sbatch -p gpu-h100 -w c318-001 --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"

# Example 5: Submit to the gpu-a100 partition and request a specific A100 node.
# export JOB=swfpn1; mkdir -p logs; sbatch -p gpu-a100 -w c316-009 --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"

# Example 6: Submit to the gpu-a100 partition, request a specific A100 node, and request 128 GB RAM.
# #SBATCH --mem=128G OR
# export JOB=swfpn1; mkdir -p logs; sbatch -p gpu-a100 -w c316-009 --mem=128G --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"

# Example 7
# Dependency Single
# export JOB=swfpn1; mkdir -p logs; sbatch --dependency=afterok:1234567 -p gpu-a100 -w c316-009 --mem=128G --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"


# Example 8
# Dependency Multiple
# export JOB=swfpn1; mkdir -p logs; sbatch --dependency=afterok:1234567:1234568:1234569 -p gpu-a100 -w c316-009 --mem=128G --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_job.sh "${JOB}.py"


# Check job status
# sacct -j job_id --format=JobID,JobName,Partition,State,ExitCode,Elapsed,Start,End


PY_SCRIPT="$1"

if [ -z "$PY_SCRIPT" ]; then
    echo "ERROR: No Python script provided."
    echo "Usage: sbatch tacc_job.sh script_name.py"
    exit 1
fi

echo "===== SLURM INFO ====="
echo "Job name: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Partition: $SLURM_JOB_PARTITION"
echo "Host: $(hostname)"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "Submit directory: $SLURM_SUBMIT_DIR"
echo "Python script: $PY_SCRIPT"
echo

cd "$SLURM_SUBMIT_DIR" || exit 1

echo "===== MODULES ====="
module load cuda/12.8
module list
echo

echo "===== CONDA ====="
# source "$WORK/shahriar/anaconda3/etc/profile.d/conda.sh"
source "$(conda info --base)/etc/profile.d/conda.sh"
conda activate mask_rcnn1

echo "Conda env: $CONDA_DEFAULT_ENV"
echo "Python path: $(which python)"
python --version
echo

echo "===== GPU CHECK ====="
nvidia-smi
echo

echo "===== PYTORCH CUDA CHECK ====="
python -c "import torch; print('torch:', torch.__version__); print('torch cuda:', torch.version.cuda); print('cuda available:', torch.cuda.is_available()); print('gpu:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
echo

echo "===== START TRAINING ====="

# Enable this for debugging CUDA errors.
# It makes CUDA operations synchronous and can slow down training.
export CUDA_LAUNCH_BLOCKING=1

python "$PY_SCRIPT"
