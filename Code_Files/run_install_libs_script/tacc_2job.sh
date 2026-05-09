#!/bin/bash
#SBATCH -N 1
#SBATCH -n 2
#SBATCH -p gpu-h100
#SBATCH --gres=gpu:2
#SBATCH --mail-user=username@gmail.com
#SBATCH --mail-type=BEGIN,END,FAIL
#SBATCH --cpus-per-task=6
#SBATCH --time=2-00:00:00
#SBATCH --job-name=two_experiments
#SBATCH --output=logs/%x.out.%j
#SBATCH --error=logs/%x.err.%j


# ============================================================
# Two independent GPU experiments in one Slurm job
# ============================================================
# Meaning:
#   -N 1              = use 1 node
#   -n 2              = run 2 Slurm tasks/processes
#   --gres=gpu:2      = request 2 GPUs total
#   --cpus-per-task=6 = give 6 CPU cores to each task
#
# Total CPU request:
#   2 tasks x 6 CPUs/task = 12 CPU cores
#
# Usage:
#   mkdir -p logs; sbatch tacc_2jobs.sh train_model_A.py train_model_B.py
#
# One-line example:
#   export JOB=two_experiments; mkdir -p logs; sbatch -p gpu-h100 -w c318-001 --job-name="$JOB" --output="logs/${JOB}.out.%j" --error="logs/${JOB}.err.%j" tacc_2jobs.sh train_model_A.py train_model_B.py
# ============================================================


# ============================================================
# Read Python scripts from command-line arguments
# ============================================================

PY_SCRIPT_1="$1"
PY_SCRIPT_2="$2"

if [ -z "$PY_SCRIPT_1" ] || [ -z "$PY_SCRIPT_2" ]; then
    echo "ERROR: Two Python scripts are required."
    echo "Usage: sbatch tacc_2jobs.sh script1.py script2.py"
    exit 1
fi


# ============================================================
# Basic Slurm information
# ============================================================

echo "===== SLURM INFO ====="
echo "Job name: $SLURM_JOB_NAME"
echo "Job ID: $SLURM_JOB_ID"
echo "Partition: $SLURM_JOB_PARTITION"
echo "Host: $(hostname)"
echo "CUDA_VISIBLE_DEVICES: $CUDA_VISIBLE_DEVICES"
echo "Submit directory: $SLURM_SUBMIT_DIR"
echo "Number of tasks: $SLURM_NTASKS"
echo "CPUs per task: $SLURM_CPUS_PER_TASK"
echo
echo "Python script 1: $PY_SCRIPT_1"
echo "Python script 2: $PY_SCRIPT_2"
echo

cd "$SLURM_SUBMIT_DIR" || exit 1

mkdir -p logs


# ============================================================
# Modules
# ============================================================

echo "===== MODULES ====="
module load cuda/12.8
module list
echo


# ============================================================
# Conda
# ============================================================

echo "===== CONDA ====="
source "$WORK/shahriar/anaconda3/etc/profile.d/conda.sh"
conda activate mask_rcnn1

echo "Conda env: $CONDA_DEFAULT_ENV"
echo "Python path: $(which python)"
python --version
echo


# ============================================================
# GPU check before training
# ============================================================

echo "===== GPU CHECK BEFORE TRAINING ====="
nvidia-smi
echo

echo "===== PYTORCH CUDA CHECK ====="
python -c "import torch; print('torch:', torch.__version__); print('torch cuda:', torch.version.cuda); print('cuda available:', torch.cuda.is_available()); print('device count:', torch.cuda.device_count()); print('gpu 0:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)"
echo


# ============================================================
# CUDA debugging
# ============================================================
# For normal training, keep this disabled because it slows training.
# Enable only when debugging CUDA errors.
# export CUDA_LAUNCH_BLOCKING=1


# ============================================================
# Start two independent experiments
# ============================================================

echo "===== START TWO EXPERIMENTS ====="
echo "Start time: $(date)"
echo

srun --exclusive -n 1 --gres=gpu:1 bash -c "
    echo '===== TASK 1 START ====='
    echo 'Host:' \$(hostname)
    echo 'CUDA_VISIBLE_DEVICES:' \$CUDA_VISIBLE_DEVICES
    nvidia-smi
    python '$PY_SCRIPT_1'
" > "logs/${SLURM_JOB_NAME}_task1_${SLURM_JOB_ID}.out" 2> "logs/${SLURM_JOB_NAME}_task1_${SLURM_JOB_ID}.err" &

PID1=$!

srun --exclusive -n 1 --gres=gpu:1 bash -c "
    echo '===== TASK 2 START ====='
    echo 'Host:' \$(hostname)
    echo 'CUDA_VISIBLE_DEVICES:' \$CUDA_VISIBLE_DEVICES
    nvidia-smi
    python '$PY_SCRIPT_2'
" > "logs/${SLURM_JOB_NAME}_task2_${SLURM_JOB_ID}.out" 2> "logs/${SLURM_JOB_NAME}_task2_${SLURM_JOB_ID}.err" &

PID2=$!


# ============================================================
# Wait for both experiments
# ============================================================

wait $PID1
STATUS1=$?

wait $PID2
STATUS2=$?

echo
echo "===== FINISHED TWO EXPERIMENTS ====="
echo "End time: $(date)"
echo "Task 1 exit status: $STATUS1"
echo "Task 2 exit status: $STATUS2"

if [ $STATUS1 -ne 0 ] || [ $STATUS2 -ne 0 ]; then
    echo "ERROR: At least one task failed."
    exit 1
fi

echo "All tasks completed successfully."