# -*- coding: utf-8 -*-
"""
Example: Optuna with extra arguments using functools.partial

pip install optuna
pip install optuna-dashboard
"""

import optuna
from functools import partial

# ===============================================
# Define a simple objective with an extra argument
# ===============================================
def objective(trial: optuna.trial.Trial, loss_weight: float):
    x = trial.suggest_float("x", -5, 5)
    # Extra argument (loss_weight) modifies the objective
    return loss_weight * (x - 2) ** 2


# ===============================================
# Example 1 — Basic study
# ===============================================
study = optuna.create_study(direction="minimize")

# Use partial to bind extra argument(s)
objective1 = partial(objective, loss_weight=1.0)
study.optimize(objective1, n_trials=20)

print("Best (weight=1.0):", study.best_params, "Value:", study.best_value)


# ===============================================
# Example 2 — Dashboard version with different args
# ===============================================
study2 = optuna.create_study(
    study_name="example_study",
    storage="sqlite:///example_study.db",  # local SQLite database
    load_if_exists=True,
    direction="minimize",
)

# Create multiple variants (like your objective1,2,3)
objective2 = partial(objective, loss_weight=0.5)
objective3 = partial(objective, loss_weight=2.0)

# Run one of them — you can run several into the same DB if you like
study2.optimize(objective3, n_trials=30)
print("Best (weight=2.0):", study2.best_params, "Value:", study2.best_value)

# ===============================================
# To visualize results:
# In terminal:  optuna-dashboard sqlite:///example_study.db
# Then open:    http://127.0.0.1:8080
# ===============================================
