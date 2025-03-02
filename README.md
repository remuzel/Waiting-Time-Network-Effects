# Waiting-Time Network Effects

This repository contains the code, data, and documentation for my Master's Thesis at Imperial College London in the Joint Mathematics and Computer Science MEng program.

## Project Overview

This project investigates network effects in ride-hailing platforms (RHPs) like Uber, Lyft, etc. through agent-based simulation. The model examines how waiting times influence market dynamics and platform competition, considering:

- How riders and drivers make decisions about which platforms to join
- The impact of network effects on market share evolution
- Platform competition dynamics with different parameters
- Comparison with real-world data from NYC's Taxi and Limousine Commission

## Repository Structure

- `/code`: Core simulation code and analysis tools
  - `main.py`: Entry point for running simulations
  - `simulator.py`: Agent-based simulator implementation
  - `agent.py`: Agent decision models for riders and drivers
  - `rhp.py`: Platform representation and dynamics
  - `requirements.txt`: Dependencies list

- `/notebooks`: Jupyter notebooks for data analysis
  - `TLC NYC Analysis`: Analysis of NYC taxi/rideshare data

- `/figures`: Visualizations from various simulation runs and data analysis
  - Contains subdirectories of experiment results by version

- `/raw`: Raw data files and simulation results
  - Includes real-world data and simulation outputs

- `/documents`: Final documentation
  - `final_report.pdf`: Complete thesis report
  - `interim_report.pdf`: Preliminary findings
  - `slides.pdf`: Presentation slides

## Getting Started

### Prerequisites

Install the required dependencies:
```
pip install -r code/requirements.txt
```

### Running Simulations

To see all available options:
```
python code/main.py --help
```

### Example Commands

Simulation with two platforms (best fit to NYC data):
```
python code/main.py --it 100 --P 2 --mu_r 0.25 0.05 --mu_d 0.9 0.2 --eta 0 0 --delay 0 65
```

Three-platform model:
```
python code/main.py --it 100 --P 3 --mu_r 0.15 0.05 0.05 --mu_d 0.9 0.1 0.2 --eta 0 0 0 --delay 0 65 65
```

## Key Parameters

- `--N`: Population size for simulation (default: 1000)
- `--P`: Number of platforms to simulate (default: 2)
- `--it`: Number of iterations for averaging (default: 1000)
- `--r`: Proportion of rider agents (default: 0.95)
- `--mu_r`: Rate at which riders leave platforms
- `--mu_d`: Rate at which drivers leave platforms
- `--eta`: Price coefficient
- `--delay`: Introduction timing for platforms (weeks)

## Data Analysis

To explore the NYC data analysis, see the Jupyter notebook at:
```
/notebooks/TLC NYC Analysis/Data Identification.ipynb
```

## Results

The simulation results demonstrate how waiting time effects influence platform competition and market share evolution. Complete findings are available in the final report.