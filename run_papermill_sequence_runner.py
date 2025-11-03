# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 21:46:22 2025

@author: Shahriar The Great

❌ Papermill only works with Jupyter notebooks (.ipynb), not plain Python .py scripts.

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

