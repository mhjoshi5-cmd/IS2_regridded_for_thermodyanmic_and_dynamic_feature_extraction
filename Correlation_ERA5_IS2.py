import xarray as xr
import pandas as pd
import numpy as np
from pyproj import Transformer
from sklearn.neighbors import KNeighborsRegressor
from scipy.stats import pearsonr

#Load ERA5 Data 
ds_era5 = xr.open_dataset("E:/Sea ice/Processed_CSVs/era5/east/2024/2024_monthly.nc")
t2m_jan = ds_era5['t2m'].isel(valid_time=2)
u10_jan = ds_era5['u10'].isel(valid_time=2)
v10_jan = ds_era5['v10'].isel(valid_time=2)

#print(ds_era5['valid_time'].isel(valid_time=0).values)

lats = ds_era5.latitude.values
lons = ds_era5.longitude.values
lon2d, lat2d = np.meshgrid(lons, lats)

# Reproject to EPSG:3031 
transformer = Transformer.from_crs("EPSG:4326", "EPSG:3031", always_xy=True)
x_flat, y_flat = transformer.transform(lon2d.flatten(), lat2d.flatten())

#Flatten and filter valid values 
t2m_flat = t2m_jan.values.flatten()
u10_flat = u10_jan.values.flatten()
v10_flat = v10_jan.values.flatten()

valid_mask_t2m = ~np.isnan(t2m_flat)
valid_mask_u10 = ~np.isnan(u10_flat)
valid_mask_v10 = ~np.isnan(v10_flat)

# Load ICESat-2 Data 
is2_df = pd.read_csv("E:/Sea ice/Processed_CSVs/25km/east/2024/Seasonal/Jan-Mar/mar_Merged_25km_with_Thickness_east24.csv")
is2_df['x'], is2_df['y'] = transformer.transform(is2_df['Longitude'].values, is2_df['Latitude'].values)

#  IDW Interpolation Function
def idw_interpolation(x_src, y_src, values, x_target, y_target, k=6, power=2):
    coords_src = np.vstack((x_src, y_src)).T
    coords_target = np.vstack((x_target, y_target)).T
    knn = KNeighborsRegressor(n_neighbors=k, weights=lambda d: 1 / (d ** power + 1e-12))
    knn.fit(coords_src, values)
    return knn.predict(coords_target)

# Interpolate ERA5 Variables to IS2 Points 
is2_df['ERA5_t2m_IDW'] = idw_interpolation(
    x_flat[valid_mask_t2m], y_flat[valid_mask_t2m], t2m_flat[valid_mask_t2m],
    is2_df['x'].values, is2_df['y'].values
)

is2_df['ERA5_u10_IDW'] = idw_interpolation(
    x_flat[valid_mask_u10], y_flat[valid_mask_u10], u10_flat[valid_mask_u10],
    is2_df['x'].values, is2_df['y'].values
)

is2_df['ERA5_v10_IDW'] = idw_interpolation(
    x_flat[valid_mask_v10], y_flat[valid_mask_v10], v10_flat[valid_mask_v10],
    is2_df['x'].values, is2_df['y'].values
)

# Correlation: Thickness vs t2m only 
valid_corr_df = is2_df.dropna(subset=["ERA5_t2m_IDW", "Thickness (m)"])
corr, pval = pearsonr(valid_corr_df["ERA5_t2m_IDW"], valid_corr_df["Thickness (m)"])

# Compute Means at IS2 Points 
mean_t2m = is2_df["ERA5_t2m_IDW"].mean()
mean_u10 = is2_df["ERA5_u10_IDW"].mean()
mean_v10 = is2_df["ERA5_v10_IDW"].mean()

# Print Results 
print(f"Correlation (Thickness vs Air Temp): {corr:.3f}")
print(f"P-value: {pval:.2e}")
print(f"Mean Air Temperature at IS2 Points (°K): {mean_t2m:.2f}")
print(f"Mean U10 at IS2 Points: {mean_u10:.2f} m/s")
print(f"Mean V10 at IS2 Points: {mean_v10:.2f} m/s")
