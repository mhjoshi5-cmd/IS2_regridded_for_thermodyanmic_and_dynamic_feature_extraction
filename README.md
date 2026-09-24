# ICESat-2 ATL10 Sea-Ice Characterization and ERA5 Atmospheric Analysis

## Research overview

This project develops a Python-based geospatial workflow to characterize Antarctic sea-ice properties from NASA's ICESat-2 ATL10 observations and investigate their relationships with atmospheric conditions from ERA5 reanalysis.

The workflow combines along-track satellite observations, statistical characterization of sea-ice morphology, spatial aggregation and atmospheric data integration.

It focuses on four related components:

* Characterization of sea-ice freeboard distributions using kernel density estimation.
* Quantification of pressure-ridge characteristics and surface roughness.
* Aggregation of satellite observations at approximately 3-km and 25-km spatial scales.
* Integration with ERA5 air temperature and wind observations for investigating relationships between sea-ice properties and atmospheric conditions.

The project supports research into sea-ice formation, growth and deformation in the Weddell Sea, Antarctica.

## 1. Research objectives

The objectives are to develop a reproducible processing workflow for characterizing sea-ice features from ICESat-2 observations, produce spatially aggregated datasets suitable for regional analysis, and investigate relationships between satellite-derived sea-ice properties and atmospheric conditions.

The workflow integrates ICESat-2 ATL10 observations with ERA5 reanalysis, enabling the examination of sea-ice variability alongside near-surface temperature and wind fields.

## 2. Data sources

### ICESat-2 ATL10

NASA's ICESat-2 ATL10 product provides the satellite observations used for sea-ice characterization. The processing workflow extracts sea-ice freeboard, geographic coordinates, along-track distances and segment lengths from the original HDF5 files. Invalid observations are removed before subsequent calculations.

### ERA5 atmospheric reanalysis

ERA5 provides atmospheric variables for investigating environmental conditions associated with the observed sea-ice properties.
Variables incorporated into the workflow include:

* 2-m air temperature
* 10-m zonal wind component
* 10-m meridional wind component

## 3. Methodology

### 3.1 Along-track processing

ICESat-2 freeboard observations are divided into approximately 3-km along-track segments.

Within each segment, freeboard distributions are characterized using kernel density estimation (KDE) to identify representative modal freeboard values.

The workflow also calculates pressure-ridge characteristics and surface roughness, providing measures of sea-ice features beyond average freeboard alone.

### 3.2 Regional spatial aggregation

The along-track measurements are aggregated into approximately 25-km latitude-based bins.

Aggregated variables include:

* Total segment length
* Average modal freeboard
* Average pressure-ridge height
* Ridge fraction
* Surface roughness

These outputs provide a spatially aggregated representation of the observed sea-ice characteristics for subsequent regional analysis.

### 3.3 Atmospheric data integration

* Processed ICESat-2 observations are spatially matched with ERA5 atmospheric fields.
* Coordinates are transformed into the Antarctic Polar Stereographic projection (EPSG:3031).
* Inverse Distance Weighting (IDW) interpolation is performed using the six nearest ERA5 grid points to estimate atmospheric variables at the satellite observation locations.
* The resulting dataset combines satellite-derived sea-ice characteristics with atmospheric information.

### 3.4 Statistical analysis

* Pearson correlation analysis is used to investigate the statistical relationship between sea-ice thickness and 2-m air temperature.
* Mean atmospheric conditions are also calculated at satellite observation locations.
* These analyses provide an initial framework for examining relationships between sea-ice properties and atmospheric variability.



## 4. Technical implementation

**Programming language:** Python

**Scientific computing:** NumPy, pandas and SciPy

**Satellite and atmospheric data processing:** h5py and xarray

**Statistical and spatial analysis:** scikit-learn and pyproj

The workflow includes HDF5 data extraction, along-track segmentation, statistical characterization, spatial aggregation, coordinate transformation and interpolation of atmospheric variables.

## 5. Example research output

A sample dataset is provided for the eastern Weddell Sea in January 2024, aggregated at approximately 25-km spatial intervals.

The dataset includes latitude, longitude, total segment length, average modal freeboard, average pressure-ridge height, ridge fraction and surface roughness.


## 6. Related research

This repository is associated with:

Joshi, M. (2025). *Analyzing Sea Ice Formation, Growth, and Deformation in the Weddell Sea, Antarctica Using ICESat-2*. Doctoral dissertation, The University of Texas at San Antonio.

It complements the [ICESat-2 Sea-Ice Thickness Pipeline](https://github.com/mhjoshi5-cmd/Sea-ice-thickness-ICESat2-pipeline), which focuses on sea-ice thickness retrieval using an improved buoyancy approach and comparisons with independent field observations.


## 7. Citation

Joshi, M. (2026). *Multiscale Sea-Ice Characterization Using ICESat-2 and ERA5*. GitHub. https://github.com/mhjoshi5-cmd/IS2_regridded_for_thermodynamic_and_dynamic_feature_extraction

## Author

**Mansi Joshi, PhD**

Geospatial Data Scientist | Satellite Remote Sensing | Sea-Ice Observations | Python
