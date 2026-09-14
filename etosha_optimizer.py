# Risk Surface Equation: (1 / ("Dist_to_Roads@1" + 1)) + (1.5 / ("Dist_to_Water@1" + 1))

import numpy as np
import rasterio
from pulp import *
import csv


raster_path = "Clean_Risk_Surface.tif"  

with rasterio.open(raster_path) as src:
  risk_matrix = src.read(1)  # Read the first band as a 2D NumPy array
  transform = src.transform
  # Handle NoData or NaN values by setting them to 0
  risk_matrix = np.nan_to_num(risk_matrix, nan=0.0)

  print(f"Raster loaded successfully! Dimensions: {risk_matrix.shape}")

# Downsample/Aggregate the grid
step = 10
sub_risk = risk_matrix[::step, ::step]
rows, cols = sub_risk.shape

print(f"Optimized grid created. Total cells to evaluate: {rows * cols}")

# Initialize the PuLP Optimization Problem
# MAXIMIZE the total risk covered by our patrols
prob = LpProblem("Etosha_AntiPoaching_Allocation", LpMaximize)

# Define Decision Variables
# x[r, c] is a binary variable: 1 if we deploy a patrol to cell (r, c), 0 otherwise.
x = {}
for r in range(rows):
  for c in range(cols):
    x[(r, c)] = LpVariable(f"patrol_{r}_{c}", cat="Binary")

# Objective Function: Maximize risk score covered
prob += lpSum(
    sub_risk[r, c] * x[(r, c)] for r in range(rows) for c in range(cols)
)

# Constraints: Resource Limitations
# Let's assume park management only has budget/personnel for 5 mobile patrol units
MAX_PATROL_UNITS = 5
prob += (
    lpSum(x[(r, c)] for r in range(rows) for c in range(cols))
    <= MAX_PATROL_UNITS
)

# Solve the Mathematical Program
print("Running optimization solver...")
prob.solve(PULP_CBC_CMD(msg=0))

print(f"Status: {LpStatus[prob.status]}")

# Safely extract objective value
obj_value = value(prob.objective)
if obj_value is not None:
  print(f"Optimal Total Risk Score Covered: {obj_value:.4f}")
else:
  print("Warning: Objective value evaluated to None (check grid values).")

# Extract the Optimal Deployment Coordinates
print("\n--- Optimal Patrol Deployment Coordinates ---")
deployment_count = 0
for r in range(rows):
  for c in range(cols):
    if x[(r, c)].varValue == 1:
      deployment_count += 1
      print(
          f"Unit {deployment_count}: Deploy to Grid Cell Row {r*step}, Column"
          f" {c*step} (Risk Value: {sub_risk[r,c]:.4f})"
      )

if deployment_count == 0:
  print(
      "Note: No units were deployed. (Check if your risk matrix values are all"
      " zero)."
  )

# Open the raster again just to grab its spatial transform matrix
with rasterio.open("Clean_Risk_Surface.tif") as src:
  transform = src.transform

with open("optimal_patrols.csv", "w", newline="") as f:
  writer = csv.writer(f)
  writer.writerow(["Longitude", "Latitude", "Risk_Value"])  # or X, Y

  for r in range(rows):
    for c in range(cols):
      if x[(r, c)].varValue == 1:
        # Scale back up from the downsampled step
        orig_row = r * step
        orig_col = c * step

        # Convert pixel row/col into map spatial coordinates (X, Y)
        x_coord, y_coord = rasterio.transform.xy(
            transform, orig_row, orig_col
        )

        writer.writerow([x_coord, y_coord, sub_risk[r, c]])

print("Exported real-world coordinate CSV successfully!")