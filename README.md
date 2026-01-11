# Homework-AI2526
Homework of Francesco Zezza (2067707) for AI course, code that implements an entire pipeline of AI experiments.
---------------------------Execution Environment---------------------------
The project requires the following software:
•	Python 3.10 or higher
•	Windows Subsystem for Linux (WSL) with Ubuntu
•	Fast Downward planner

------------------------------Fast Downward setup-------------------------------
Fast Downward must be installed inside the WSL environment.
In particular, the planner is expected to be located at:
$HOME/tools/downward/fast-downward.py
This can be achieved by cloning the official Fast Downward repository inside the WSL home directory.

-----------------------------Running the experiments----------------------------
When running the experiments on Windows, the Python module search path must be set as follows:
$env:PYTHONPATH="src"
Afterwards, the full experimental evaluation can be launched from the project root directory with:
python scripts/run_experiments.py
The script automatically generates problem instances, runs both A* and the planning-based approach, and stores the collected metrics in CSV format.

--------------------------------Execution Time---------------------------------
Depending on the selected parameters, the complete execution may take a non-negligible amount of time.
On the reference machine used for this project, generating the full set of experimental results required approximately 25/30 minutes.

------------------------------------Output--------------------------------------
Experimental results are saved in:
results/runs.csv
These results can be used to reproduce the experimental analysis