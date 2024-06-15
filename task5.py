import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

# Load a sample of the dataset
file_path = 'US_Accidents_March23.csv'
df = pd.read_csv(file_path, nrows=100000)  # Load first 100,000 rows as a sample

# Convert date-time columns
df['Start_Time'] = pd.to_datetime(df['Start_Time'], errors='coerce')
df['End_Time'] = pd.to_datetime(df['End_Time'], errors='coerce')
df['Weather_Timestamp'] = pd.to_datetime(df['Weather_Timestamp'], errors='coerce')

# Drop rows with NaT in date-time columns
df_clean = df.dropna(subset=['Start_Time', 'End_Time'])

# Add additional time-related columns using .loc to avoid SettingWithCopyWarning
df_clean.loc[:, 'Year'] = df_clean['Start_Time'].dt.year
df_clean.loc[:, 'Month'] = df_clean['Start_Time'].dt.month
df_clean.loc[:, 'DayOfWeek'] = df_clean['Start_Time'].dt.dayofweek
df_clean.loc[:, 'Hour'] = df_clean['Start_Time'].dt.hour

# Visualize accident severity distribution
plt.figure(figsize=(10, 6))
sns.countplot(data=df_clean, x='Severity')
plt.title('Distribution of Accident Severity')
plt.xlabel('Severity')
plt.ylabel('Count')
plt.show()

# Visualize accident hotspots using a heatmap (using a sample for faster processing)
map_center = [df_clean['Start_Lat'].mean(), df_clean['Start_Lng'].mean()]
accident_map = folium.Map(location=map_center, zoom_start=5)

# Prepare data for heatmap (using a sample)
heat_data = [[row['Start_Lat'], row['Start_Lng']] for index, row in df_clean.iterrows()]

# Add heatmap layer
HeatMap(heat_data).add_to(accident_map)

# Save the heatmap as HTML
heatmap_file = 'accident_hotspots.html'
accident_map.save(heatmap_file)
print(f"Accident hotspots map saved as '{heatmap_file}'")

# Display other relevant plots or visualizations here

# Example: Visualize accident counts by weather condition
plt.figure(figsize=(12, 6))
sns.countplot(data=df_clean, y='Weather_Condition', order=df_clean['Weather_Condition'].value_counts().index[:10])
plt.title('Top 10 Weather Conditions During Accidents')
plt.xlabel('Count')
plt.ylabel('Weather Condition')
plt.tight_layout()
plt.show()
