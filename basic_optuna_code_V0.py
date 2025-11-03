# -*- coding: utf-8 -*-
"""
Created on Mon Nov  3 14:51:22 2025

@author: kec994

pip install optuna
pip install optuna-dashboard


"""



import optuna

def objective(trial: optuna.trial.Trial):
    x = trial.suggest_float("x", -5, 5)
    return (x - 2) ** 2

study = optuna.create_study(direction="minimize")
study.optimize(objective, n_trials=20)
print("Best:", study.best_params, "Value:", study.best_value)




# Using Dashboard *******************************

import optuna

# Create a study stored in an SQLite file
study = optuna.create_study(
    study_name="example_study",
    storage="sqlite:///example_study.db",  # local DB file
    load_if_exists=True,
)

def objective(trial):
    x = trial.suggest_float("x", -10, 10)
    return (x - 2) ** 2

study.optimize(objective, n_trials=50)

# 🖥️ 3. Launch the dashboard : In your terminal or Anaconda Prompt:
# optuna-dashboard sqlite:///example_study.db
#Then open the link it shows — typically: http://127.0.0.1:8080



#OR


# Terminal 1
#optuna-dashboard sqlite:///example_study.db

# Terminal 2 (run your Python script)
#python optimize_script.py
