import os
import json
import matplotlib.pyplot as plt
from collections import defaultdict

# Load JSON data
def load_data(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

# Ensure "pie_charts" folder exists
OUTPUT_FOLDER = "pie_charts"
if os.path.exists(OUTPUT_FOLDER):
    for file in os.listdir(OUTPUT_FOLDER):
        os.remove(os.path.join(OUTPUT_FOLDER, file))
else:
    os.makedirs(OUTPUT_FOLDER)

# Function to create and save pie charts
def create_pie_chart(data, labels, title, filename):
    plt.figure(figsize=(8, 8))
    colors = plt.cm.Paired.colors[:len(labels)]  # Assign unique colors
    wedges, texts, autotexts = plt.pie(
        data, labels=None, autopct=lambda p: f'{p:.1f}%' if p > 0 else '', 
        startangle=140, colors=colors, pctdistance=1.2)  # Moves percentages outside slices

    # Format percentage labels above slices
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(10)
        autotext.set_weight('bold')
    
    plt.title(title)
    
    # Improved legend placement in the lower-left corner
    plt.legend(wedges, labels, title="Legend", loc="lower left", bbox_to_anchor=(-0.4, 0))
    
    plt.savefig(os.path.join(OUTPUT_FOLDER, filename), bbox_inches='tight')
    plt.close()

# Process earthquake data
def process_data(data):
    city_counts = defaultdict(int)
    magnitude_ranges = {"<=2.0": 0, "2.1-3.0": 0, "3.1-5.0": 0, ">5.0": 0}
    magnitude_by_city = defaultdict(lambda: {"<=2.0": 0, "2.1-3.0": 0, "3.1-5.0": 0, ">5.0": 0})
    year_counts = defaultdict(int)
    month_counts = defaultdict(int)
    time_of_day_counts = {"Morning": 0, "Afternoon": 0, "Evening": 0, "Night": 0}
    time_of_day_by_city = defaultdict(lambda: {"Morning": 0, "Afternoon": 0, "Evening": 0, "Night": 0})
    elevation_ranges = {"<=10": 0, "11-80": 0, "81-200": 0, ">=200": 0}
    
    for entry in data:
        city = entry["city"]
        magnitude = entry["magnitude"]
        year = entry["date"].split("-")[0]
        month = entry["date"].split("-")[1]
        hour = int(entry["time"].split(":")[0])
        elevation = entry["elevation"]
        
        # City counts
        city_counts[city] += 1
        
        # Magnitude ranges
        if magnitude <= 2.0:
            magnitude_ranges["<=2.0"] += 1
            magnitude_by_city[city]["<=2.0"] += 1
        elif 2.1 <= magnitude <= 3.0:
            magnitude_ranges["2.1-3.0"] += 1
            magnitude_by_city[city]["2.1-3.0"] += 1
        elif 3.1 <= magnitude <= 5.0:
            magnitude_ranges["3.1-5.0"] += 1
            magnitude_by_city[city]["3.1-5.0"] += 1
        else:
            magnitude_ranges[">5.0"] += 1
            magnitude_by_city[city][">5.0"] += 1
        
        # Year and month counts
        year_counts[year] += 1
        month_counts[month] += 1
        
        # Time of day
        if 0 <= hour < 12:
            time_of_day_counts["Morning"] += 1
            time_of_day_by_city[city]["Morning"] += 1
        elif 12 <= hour < 15:
            time_of_day_counts["Afternoon"] += 1
            time_of_day_by_city[city]["Afternoon"] += 1
        elif 15 <= hour < 19:
            time_of_day_counts["Evening"] += 1
            time_of_day_by_city[city]["Evening"] += 1
        else:
            time_of_day_counts["Night"] += 1
            time_of_day_by_city[city]["Night"] += 1
        
        # Elevation ranges
        if elevation <= 10:
            elevation_ranges["<=10"] += 1
        elif 11 <= elevation <= 80:
            elevation_ranges["11-80"] += 1
        elif 81 <= elevation <= 200:
            elevation_ranges["81-200"] += 1
        else:
            elevation_ranges[">=200"] += 1

    return city_counts, magnitude_ranges, magnitude_by_city, year_counts, month_counts, time_of_day_counts, time_of_day_by_city, elevation_ranges

# Generate pie charts
def generate_charts(data):
    city_counts, magnitude_ranges, magnitude_by_city, year_counts, month_counts, time_of_day_counts, time_of_day_by_city, elevation_ranges = process_data(data)
    
    create_pie_chart(city_counts.values(), city_counts.keys(), "Earthquake Distribution by City", "city_distribution.png")
    create_pie_chart(magnitude_ranges.values(), magnitude_ranges.keys(), "Earthquake Magnitude Distribution", "magnitude_distribution.png")
    create_pie_chart(year_counts.values(), year_counts.keys(), "Earthquakes by Year", "year_distribution.png")
    create_pie_chart(month_counts.values(), month_counts.keys(), "Earthquakes by Month", "month_distribution.png")
    create_pie_chart(time_of_day_counts.values(), time_of_day_counts.keys(), "Earthquakes by Time of Day", "time_distribution.png")
    create_pie_chart(elevation_ranges.values(), elevation_ranges.keys(), "Earthquakes by Elevation", "elevation_distribution.png")
    
    for city, magnitudes in magnitude_by_city.items():
        create_pie_chart(magnitudes.values(), magnitudes.keys(), f"Magnitude Distribution in {city}", f"magnitude_{city}.png")
    
    for city, times in time_of_day_by_city.items():
        create_pie_chart(times.values(), times.keys(), f"Time Distribution in {city}", f"time_{city}.png")

# Main Execution
json_file = "displayfiles//merged_data.json"
data = load_data(json_file)
generate_charts(data)
