# Spatial Optimization for Wildlife Protection using Python and QGIS

An end-to-end Geographic Information Systems (GIS) and Operations Research project that frames wildlife protection as a constrained mathematical optimization problem. Using open-source spatial data and Python, this model calculates the optimal deployment strategy for anti-poaching resources across a massive, complex ecosystem.

Project Overview
Protecting wildlife in vast reserves like Etosha National Park (Namibia, roughly 22,000 square kilometers) presents a severe resource-allocation challenge. Human personnel, vehicles, and technological assets are strictly limited, while threats are distributed across thousands of square kilometers. 

Instead of relying on intuition, this project builds a data-driven optimization pipeline that:
1. Quantifies Risk: Transforms raw landscape features (roads, water bodies, and topography) into a continuous mathematical Risk Surface.
2. Solves Resource Constraints: Uses Mixed-Integer Linear Programming (MILP) to find the exact configuration of patrol units that maximizes total threat coverage under strict budget and capacity limits.

The Modeling and Computational Approach

1. Spatial Preprocessing and Distance-Decay (GIS)
Using QGIS, vector data from OpenStreetMap was converted into continuous distance-decay raster surfaces:
- Road Proximity (Dist_to_Roads): Models human accessibility and entry vectors for illegal intrusion.
- Water Proximity (Dist_to_Water): Models resource-attraction mechanics, recognizing waterholes as ecological bottlenecks where wildlife and poachers intersect.

These matrices were combined using a normalized inverse-distance decay equation inside a Raster Calculator to generate a continuous Risk Surface (Clean_Risk_Surface.tif).

2. Mathematical Formulation (Operations Research)
The deployment problem is modeled as a Maximum Coverage Location Problem (MCLP):
- Decision Variables: Binary variables representing whether a patrol unit is deployed to a specific grid cell (1 for yes, 0 for no).
- Objective Function: Maximize the cumulative risk score covered by the deployed units.
- Constraints: Total deployed units cannot exceed available operational capacity.

3. Computational Solution Engine (Python)
The script uses Rasterio to load the spatial matrix, NumPy to handle matrix downsampling for computational efficiency, and PuLP (utilizing the CBC solver) to solve the Mixed-Integer Program to mathematical optimality.

Visualizing the Risk Landscape

Below is the generated spatial risk map of Etosha National Park. High-threat zones concentrate heavily along accessible infrastructure and water boundaries, while remote interiors represent lower immediate threat gradients.

![Etosha Risk Surface Map](images/etosha_risk_map.png)
(Note: Ensure your map image is saved as etosha_risk_map.png inside the images directory).

Getting Started and Instructions

Prerequisites
Make sure you have Python installed along with the required geospatial and optimization packages:
pip install numpy rasterio pulp matplotlib

Repository Structure
Wildlife Reserve Protection Planning/
├── images/
│   └── etosha_risk_map.png     # Visual map outputs
├── Clean_Risk_Surface.tif      # Spatial risk matrix (GIS raster)
├── etosha_optimizer.py         # Main computational optimization script
└── README.md                   # Project documentation

Running the Optimization Script
1. Ensure your Clean_Risk_Surface.tif and etosha_optimizer.py are in the same directory.
2. Run the script via your terminal:
python etosha_optimizer.py
3. The script will output the solver status, optimal objective score, and exact matrix coordinates for your patrol deployments.

Key Takeaways and Skills Demonstrated
- Spatial Data Engineering: Rasterizing vector networks, calculating proximity distance gradients, and raster calculator modeling.
- Operations Research: Formulating real-world conservation logistics into mathematical objective functions and binary constraints.
- Scientific Computing: Bridging GIS spatial file formats with linear programming solvers in Python.
