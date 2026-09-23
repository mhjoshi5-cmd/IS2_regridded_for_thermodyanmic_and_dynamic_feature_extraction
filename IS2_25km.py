import os
import h5py
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from scipy.signal import find_peaks
# Define the folder containing ATL10 HDF5 files
folder_path = "D:/Sea ice/IS2 raw data/2024/west/aug"  # Change this to your folder path
output_folder_25km = "D:/Sea ice/Processed_CSVs/25km/west/2024/aug/gt3l"
output_folder_3km="D:/Sea ice/Processed_CSVs/3km/west/2024/aug/gt3l"
os.makedirs(output_folder_25km, exist_ok=True)
os.makedirs(output_folder_3km, exist_ok=True)

'''
def is_bimodal(data, bandwidth=0.5, peak_prominence=0.01):
    """
    Determine if the data distribution is bimodal using KDE and peak detection.

    Parameters:
        data (array-like): The input data to check.
        bandwidth (float): Bandwidth for the KDE.
        peak_prominence (float): Minimum prominence of peaks to count.

    Returns:
        bool: True if the data is bimodal (i.e., has two significant peaks), False otherwise.
        int: Number of detected peaks.
    """
    if len(data) < 10:
        return False, 0  # Too little data to reliably detect modes

    kde = gaussian_kde(data, bw_method=bandwidth)
    x_vals = np.linspace(data.min(), data.max(), 1000)
    kde_vals = kde(x_vals)

    # Find peaks
    peaks, _ = find_peaks(kde_vals, prominence=peak_prominence)
    
    return len(peaks) == 2, len(peaks)
'''

# Initialize list to store data from multiple files
all_25km_data = []

# Loop through each HDF5 file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".h5"):  # Only process HDF5 files
        file_path = os.path.join(folder_path, filename)
        print(f"Processing: {filename}")

        # Open the HDF5 file and extract relevant datasets
        with h5py.File(file_path, "r") as hdf:
            try:
                #freeboard = np.array(hdf["gt3l/freeboard_beam_segment/beam_freeboard/beam_fb_height"])
                #along_track_distance = np.array(hdf["gt3l/freeboard_beam_segment/beam_freeboard/seg_dist_x"])
                #latitude = np.array(hdf["gt3l/freeboard_beam_segment/beam_freeboard/latitude"])
                #longitude = np.array(hdf["gt3l/freeboard_beam_segment/beam_freeboard/longitude"])
                #height_segment_length = np.array(hdf["gt3l/freeboard_beam_segment/height_segments/height_segment_length_seg"]) 
                #version 6
                freeboard=np.array(hdf['/gt3l/freeboard_segment/beam_fb_height'])
                along_track_distance = np.array(hdf["gt3l/freeboard_segment/seg_dist_x"])
                latitude=np.array(hdf['/gt3l/freeboard_segment/latitude'])
                longitude=np.array(hdf['/gt3l/freeboard_segment/longitude'])
                height_segment_length=np.array(hdf['/gt3l/freeboard_segment/heights/height_segment_length_seg'])
            except KeyError as e:
                print(f"Missing dataset in {filename}: {e}. Skipping file.")
                continue
                
                

                
            
        # Convert along-track distance to km
        along_track_distance_km = (along_track_distance - along_track_distance[0]) / 1000

        # Filter out invalid data
        valid_mask = (freeboard > 0) & (freeboard < 2)
        freeboard_filtered = freeboard[valid_mask]
        along_track_distance_km_filtered = along_track_distance_km[valid_mask]
        latitude_filtered = latitude[valid_mask]
        longitude_filtered = longitude[valid_mask]
        height_seg_len = height_segment_length[valid_mask]

        # Check if filtering removed all data
        if freeboard_filtered.size == 0:
            print(f"Warning: No valid freeboard data in {filename}. Skipping file.")
            continue  # Skip to next file
        
        # Define 3-km segments
        segment_boundaries = np.arange(along_track_distance_km_filtered.min(), along_track_distance_km_filtered.max(), 3)

        # Initialize lists for 3-km segments
        modal_freeboards = []
        pressure_ridges_avg = []
        ridge_fractions = []
        ridge_lengths = []
        total_segment_lengths = []
        surface_roughness_values = []
        segment_endpoints = []
        segment_latitudes = []
        segment_longitudes = []

        # Process each 3-km segment independently
        for i in range(len(segment_boundaries) - 1):
            segment_mask = (along_track_distance_km_filtered >= segment_boundaries[i]) & \
                           (along_track_distance_km_filtered < segment_boundaries[i + 1])
            segment_data = freeboard_filtered[segment_mask]
            #bimodal, num_peaks = is_bimodal(segment_data)
            #print(f"Segment {i}: Bimodal={bimodal}, Peaks={num_peaks}")
            segment_lat = latitude_filtered[segment_mask]
            segment_lon = longitude_filtered[segment_mask]
            segment_distances = height_seg_len[segment_mask]

            if len(segment_data) < 10:
                continue  # Skip segments with insufficient data

            # Compute KDE for modal freeboard
            kde_segment = gaussian_kde(segment_data, bw_method=0.1)
            segment_range = np.linspace(segment_data.min(), segment_data.max(), 500)
            kde_values_segment = kde_segment(segment_range)
            modal_freeboard_segment = segment_range[np.argmax(kde_values_segment)]
            if modal_freeboard_segment <= 0.15:
                continue

            # Identify pressure ridges
            ridge_mask = segment_data > (modal_freeboard_segment + 0.6)
            pressure_ridge_values = segment_data[ridge_mask]
            ridge_distances = segment_distances[ridge_mask]
            ridge_length = np.sum(ridge_distances)

            # Compute total segment length
            total_segment_length = np.sum(segment_distances)

            # Compute ridge fraction
            ridge_fraction = (ridge_length / total_segment_length) * 100 if total_segment_length > 0 else 0

            # Compute surface roughness
            surface_roughness = np.std(segment_data)

            # Compute the average pressure ridge value
            pressure_ridge_avg = np.nan if len(pressure_ridge_values) == 0 else np.mean(pressure_ridge_values)

            # Store results per segment
            modal_freeboards.append(modal_freeboard_segment)
            pressure_ridges_avg.append(pressure_ridge_avg)
            ridge_fractions.append(ridge_fraction)
            ridge_lengths.append(ridge_length)
            total_segment_lengths.append(total_segment_length)
            surface_roughness_values.append(surface_roughness)
            segment_endpoints.append(segment_boundaries[i + 1])  # Store endpoint
            segment_latitudes.append(segment_lat[-1])  # Last latitude in segment
            segment_longitudes.append(segment_lon[-1])  # Last longitude in segment

        # If no valid segments were found, skip this file
        if len(modal_freeboards) == 0:
            print(f"Warning: No valid 3-km segments found in {filename}. Skipping file.")
            continue

        # Create DataFrame for 3-km segments
        df_combined = pd.DataFrame({
            "Segment Endpoint (km)": segment_endpoints,
            "Latitude": segment_latitudes,
            "Longitude": segment_longitudes,
            "Modal Freeboard (m)": modal_freeboards,
            "Average Pressure Ridge (m)": pressure_ridges_avg,
            "Ridge Fraction (%)": ridge_fractions,
            "Ridge Length (m)": ridge_lengths,
            "Total Segment Length (m)": total_segment_lengths,
            "Surface Roughness (m)": surface_roughness_values
        })
        output_csv_individual1 = os.path.join(output_folder_3km, filename.replace(".h5", "_3km.csv"))
        df_combined.to_csv(output_csv_individual1, index=False)
        #print(f"Saved individual 25-km CSV: {output_csv_individual1}")
        #all_25km_data.append(df_25km_grid)

        print(f"Processed successfully: {filename}")

        # Define 25-km grid bins based on latitude
        grid_size_km = 25
        lat_bins = np.arange(df_combined["Latitude"].min(), df_combined["Latitude"].max(), grid_size_km / 111)

        grid_latitudes, grid_longitudes = [], []
        grid_segment_lengths, grid_modal_freeboards = [], []
        grid_pressure_ridges, grid_ridge_fractions, grid_surface_roughness = [], [], []

        # Process 25-km grid cells
        for i in range(len(lat_bins) - 1):
            bin_mask = (df_combined["Latitude"] >= lat_bins[i]) & (df_combined["Latitude"] < lat_bins[i + 1])
            bin_values = df_combined.loc[bin_mask]

            if len(bin_values) > 0:
                total_length = len(bin_values) * 3
                weighted_avg_freeboard = np.sum(bin_values["Modal Freeboard (m)"] * 3) / total_length
                weighted_avg_pressure_ridge = np.nanmean(bin_values["Average Pressure Ridge (m)"])
                weighted_avg_ridge_fraction = np.nanmean(bin_values["Ridge Fraction (%)"])
                weighted_avg_surface_roughness = np.nanmean(bin_values["Surface Roughness (m)"])

                # Store 25-km grid values
                grid_latitudes.append(np.nanmean(bin_values["Latitude"]))
                grid_longitudes.append(np.nanmean(bin_values["Longitude"]))
                grid_segment_lengths.append(total_length)
                grid_modal_freeboards.append(weighted_avg_freeboard)
                grid_pressure_ridges.append(weighted_avg_pressure_ridge)
                grid_ridge_fractions.append(weighted_avg_ridge_fraction)
                grid_surface_roughness.append(weighted_avg_surface_roughness)
        df_25km_grid = pd.DataFrame({
            "Latitude": grid_latitudes,
            "Longitude": grid_longitudes,
            "Total Segment Length (km)": grid_segment_lengths,
            "Average Modal Freeboard (m)": grid_modal_freeboards,
            "Average Pressure Ridge (m)": grid_pressure_ridges,
            "Ridge Fraction (%)": grid_ridge_fractions,
            #"Mean Ridge Height (m)": grid_mean_ridge_heights,
            "Surface Roughness (m)": grid_surface_roughness
        })
        output_csv_individual = os.path.join(output_folder_25km, filename.replace(".h5", "_25km.csv"))
        df_25km_grid.to_csv(output_csv_individual, index=False)
        print(f"Saved individual 25-km CSV: {output_csv_individual}")
        #all_25km_data.append(df_25km_grid)

        print(f"Processed successfully: {filename}")
        
        
        df_25km_grid["File"] = filename  # Add filename column
        all_25km_data.append(df_25km_grid)
df_combined_25km = pd.concat(all_25km_data, ignore_index=True)

# Save the final combined 25-km dataset to CSV
output_csv_path ="D:/Sea ice/Processed_CSVs/25km/west/2024/aug/Combined_25km_aug24_gt3l.csv"
df_combined_25km.to_csv(output_csv_path, index=False)

print(f"Processing complete. Combined 25-km data saved to: {output_csv_path}")

