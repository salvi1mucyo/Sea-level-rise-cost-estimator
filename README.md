# 🌊 Sea Level Rise Simulation – 6.100B Fall 2024

This project predicts sea level rise from 2030 to 2100 and simulates its economic impact on property damage using multiple strategies. It uses historical data to forecast trends and performs Monte Carlo simulations to compare different insurance decisions.

## 📁 Files

- `sea_level_rise.py`: Main Python script with data loading, prediction, and simulation logic.
- `sea_level_change.csv`: Input dataset containing projected sea level rise and standard deviations (not included here).

## 📊 Features

- Load and interpolate sea level rise data
- Predict annual and cumulative sea level changes
- Run Monte Carlo simulations for 500 scenarios
- Visualize results through plots
- Compare 3 financial strategies:
  - No insurance
  - Insure immediately
  - Invest and insure later

## 📦 Requirements

- Python 3.6+
- NumPy
- Matplotlib

Install dependencies with:

```bash
pip install numpy matplotlib
