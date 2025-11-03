# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 21:46:22 2025

@author: Shahriar The Great

❌ Papermill only works with Jupyter notebooks (.ipynb), not plain Python .py scripts.

If you want to input arguments then add first code cell like this:

# Parameters
run_name = "default_run"
batch_size = 8
epochs = 100
scheduler_option = 4
learning_rate = 1e-3




pip install papermill
python run_papermill_sequence_runner.py

"""

import papermill as pm
from datetime import datetime
from pathlib import Path

NOTEBOOKS = [
    "V1.0_Lipschitz_3ch.ipynb",
    "V1.0_Lipschitz_6ch.ipynb",
    "V1.0_RedPlat_3ch.ipynb",
    "V1.0_RedPlat_6ch.ipynb",
]

output_dir = Path("executed_notebooks")
output_dir.mkdir(exist_ok=True)



print(f"=== Run started {datetime.now():%Y-%m-%d %H:%M:%S} ===")
for nb in NOTEBOOKS:
    input_path = Path(nb)
    output_path = output_dir / input_path.name.replace(".ipynb", f"-executed.ipynb")

    print(f"\n▶ Running {input_path.name} ...")
    pm.execute_notebook(
        input_path,
        output_path,
        parameters={},   # You can pass variables here if needed
        kernel_name=None,  # or specify e.g. "python3"
        progress_bar=True
    )
    print(f"✅ Done: {output_path}")
print(f"\n=== All notebooks completed at {datetime.now():%Y-%m-%d %H:%M:%S} ===")




# Example — passing different params per notebook *************************************************
NOTEBOOKS = {
    "V1.0_Lipschitz_3ch.ipynb": {"run_name": "Lipschitz_3ch", "in_ch": 3},
    "V1.0_Lipschitz_6ch.ipynb": {"run_name": "Lipschitz_6ch", "in_ch": 6},
    "V1.0_RedPlat_3ch.ipynb": {"run_name": "RedPlat_3ch", "in_ch": 3},
    "V1.0_RedPlat_6ch.ipynb": {"run_name": "RedPlat_6ch", "in_ch": 6},
}

print(f"=== Run started {datetime.now():%Y-%m-%d %H:%M:%S} ===")
for nb, params in NOTEBOOKS.items():
    input_path = Path(nb)
    output_path = output_dir / input_path.name.replace(".ipynb", "-executed.ipynb")

    print(f"\n▶ Running {input_path.name} ...")
    pm.execute_notebook(
        input_path,
        output_path,
        parameters=params,
        kernel_name=None, # or "python3"
        progress_bar=True
    )
    print(f"✅ Done: {output_path}")
print(f"\n=== All notebooks completed at {datetime.now():%Y-%m-%d %H:%M:%S} ===")



# Same file different parameters **************************************
# Run multiple notebooks (even the same one) with different parameters using Papermill.


# --- Configuration ---
NOTEBOOKS = {
    "V1.0_Lipschitz_3ch.ipynb": [
        {"run_name": "Lipschitz_3ch", "in_ch": 3},
        {"run_name": "Lipschitz_6ch", "in_ch": 6},
    ],
    "V1.0_RedPlat_3ch.ipynb": [
        {"run_name": "RedPlat_3ch", "in_ch": 3},
        {"run_name": "RedPlat_6ch", "in_ch": 6},
    ]
}

output_dir = Path("executed_notebooks")
output_dir.mkdir(exist_ok=True)


# --- Run sequence ---
print(f"=== Run started {datetime.now():%Y-%m-%d %H:%M:%S} ===")
for nb, runs in NOTEBOOKS.items():
    for params in runs:
        run_name = params["run_name"]
        output_path = output_dir / f"{Path(nb).stem}_{run_name}-executed.ipynb"

        print(f"\n▶ Running {nb} ({run_name}) ...")
        pm.execute_notebook(
            nb,
            output_path,
            parameters=params,
            kernel_name=None,   # or "python3"
            progress_bar=True
        )
        print(f"✅ Done: {output_path}")
print(f"\n=== All notebooks completed at {datetime.now():%Y-%m-%d %H:%M:%S} ===")
