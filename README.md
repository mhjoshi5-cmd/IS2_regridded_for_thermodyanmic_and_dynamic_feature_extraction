# ICESat-2 ATL10 Sea-Ice Characterization and ERA5 Atmospheric Analysis
# Overview

This project develops a Python-based processing and analysis workflow for investigating sea-ice freeboard, pressure ridging, surface roughness, and sea-ice thickness using NASA's ICESat-2 ATL10 product, together with atmospheric conditions from the ERA5 reanalysis.
The workflow processes raw ICESat-2 ATL10 HDF5 files, extracts freeboard observations, identifies representative modal freeboard values, characterizes pressure ridges and surface roughness along the satellite ground track, and aggregates the observations to approximately 3-km and 25-km spatial scales.
The processed ICESat-2 observations are subsequently spatially matched with ERA5 atmospheric variables to investigate relationships between sea-ice properties and atmospheric conditions.

# Methodology

## 1. ICESat-2 ATL10 Data Processing

Raw ATL10 HDF5 files are processed to extract sea-ice freeboard, geographic coordinates, along-track distances, and segment lengths. Invalid observations are filtered before further analysis.

## 2. Sea-Ice Characterization

Freeboard observations are divided into approximately 3-km along-track segments. Kernel Density Estimation (KDE) is used to determine modal freeboard, while pressure-ridge characteristics and surface roughness are calculated for each segment.

The resulting measurements are aggregated into approximately 25-km latitude-based bins for regional analysis.

## 3. ERA5 Data Integration

ERA5 atmospheric variables, including 2-m air temperature and 10-m wind components, are spatially matched with processed ICESat-2 observations.

Coordinates are transformed into the Antarctic Polar Stereographic projection (EPSG:3031). Inverse Distance Weighting (IDW), using the six nearest ERA5 grid points, is applied to interpolate atmospheric variables to the ICESat-2 observation locations.

## 4. Statistical Analysis

Pearson correlation analysis is performed to investigate the relationship between sea-ice thickness and air temperature. Mean atmospheric conditions are also calculated at the satellite observation locations.

# Tools and Technologies

Python, NumPy, pandas, h5py, xarray, SciPy, scikit-learn, and pyproj.

# Related publication:
Joshi, M. (2025). Analyzing Sea Ice Formation, Growth, and Deformation in the Weddell Sea, Antarctica Using ICESat-2 (Doctoral dissertation, The University of Texas at San Antonio).

If you use this code, please cite:

Joshi, M. (2026). GitHub: https://github.com/mhjoshi5-cmd/IS2_regridded_for_thermodyanmic_and_dynamic_feature_extraction 



