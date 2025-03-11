import json
import matplotlib.pyplot as plt
from collections import defaultdict
import datetime
import os

# Helper function to load JSON data
def load_data(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# Helper function to create a pie chart
def create_pie_chart(data, labels, title, filename):
    # Ensure the pie_charts folder exists
    if not os.path.exists('pie_charts'):
        os.makedirs('pie_charts')

    plt.figure(figsize=(7, 7))
    plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title(title)
    plt.axis('equal')
    plt.savefig(f'pie_charts/{filename}')
    plt.close()

# Helper function to convert time to hours (HH format)
def get_hour_from_time(time_str):
    return int(time_str.split(":")[0])

# Helper function to categorize hours
def categorize_time_of_day(hour):
    if 0 <= hour <= 9:
        return "morning"
    elif 10 <= hour <= 12:
        return "mid_morning"
    elif 13 <= hour <= 16:
        return "afternoon"
    elif 17 <= hour <= 19:
        return "evening"
    else:
        return "night"

# Categorize data based on conditions
def categorize_entry(entry):
    # Elevation
    if entry['elevation'] <= 10:
        entry['elevation_category'] = 'below sea-level'
    elif 11 <= entry['elevation'] <= 30:
        entry['elevation_category'] = 'sea-level'
    elif 31 <= entry['elevation'] <= 60:
        entry['elevation_category'] = 'ground_level'
    elif 61 <= entry['elevation'] <= 90:
        entry['elevation_category'] = 'ground_level_mid'
    else:
        entry['elevation_category'] = 'ground_level_high'

    # Magnitude
    if entry['magnitude'] <= 2:
        entry['magnitude_category'] = 'low_mag'
    elif 3 <= entry['magnitude'] <= 5:
        entry['magnitude_category'] = 'medium_mag'
    else:
        entry['magnitude_category'] = 'high_mag'

    # Rain Sum
    if entry['weather']['rain_sum'] <= 5:
        entry['rain_category'] = 'rain_sum_low'
    elif 6 <= entry['weather']['rain_sum'] <= 10:
        entry['rain_category'] = 'rain_sum_medium'
    else:
        entry['rain_category'] = 'rain_sum_high'

    # Time of Day
    hour = get_hour_from_time(entry['time'])
    entry['time_of_day'] = categorize_time_of_day(hour)

    # Date for monthly and yearly categorization
    date = datetime.datetime.strptime(entry['date'], "%Y-%m-%d")
    entry['year'] = date.year
    entry['month'] = date.month

    return entry

# Create pie charts based on categories
def analyze_and_create_charts(data):
    # For each entry, categorize and add the category to the entry
    categorized_entries = [categorize_entry(entry) for entry in data]

    # 1. Time of Day Distribution
    time_of_day_count = defaultdict(int)
    for entry in categorized_entries:
        time_of_day_count[entry['time_of_day']] += 1
    time_of_day_labels = time_of_day_count.keys()
    time_of_day_data = time_of_day_count.values()
    create_pie_chart(time_of_day_data, time_of_day_labels, "Time of Day Distribution", "time_of_day_distribution.png")

    # 2. Magnitude Distribution
    magnitude_count = defaultdict(int)
    for entry in categorized_entries:
        magnitude_count[entry['magnitude_category']] += 1
    magnitude_labels = magnitude_count.keys()
    magnitude_data = magnitude_count.values()
    create_pie_chart(magnitude_data, magnitude_labels, "Magnitude Distribution", "magnitude_distribution.png")

    # 3. Elevation Category Distribution
    elevation_count = defaultdict(int)
    for entry in categorized_entries:
        elevation_count[entry['elevation_category']] += 1
    elevation_labels = elevation_count.keys()
    elevation_data = elevation_count.values()
    create_pie_chart(elevation_data, elevation_labels, "Elevation Category Distribution", "elevation_category_distribution.png")

    # 4. Rainfall Category Distribution
    rain_count = defaultdict(int)
    for entry in categorized_entries:
        rain_count[entry['rain_category']] += 1
    rain_labels = rain_count.keys()
    rain_data = rain_count.values()
    create_pie_chart(rain_data, rain_labels, "Rainfall Category Distribution", "rainfall_category_distribution.png")

    # 5. Yearly Distribution
    yearly_count = defaultdict(int)
    for entry in categorized_entries:
        yearly_count[entry['year']] += 1
    yearly_labels = sorted(yearly_count.keys())
    yearly_data = [yearly_count[year] for year in yearly_labels]
    create_pie_chart(yearly_data, yearly_labels, "Yearly Distribution", "yearly_distribution.png")

    # 6. Monthly Distribution
    monthly_count = defaultdict(int)
    for entry in categorized_entries:
        monthly_count[entry['month']] += 1
    monthly_labels = sorted(monthly_count.keys())
    monthly_data = [monthly_count[month] for month in monthly_labels]
    create_pie_chart(monthly_data, monthly_labels, "Monthly Distribution", "monthly_distribution.png")

    # 7. Time of Day Distribution by Magnitude
    time_of_day_by_magnitude = defaultdict(lambda: defaultdict(int))
    for entry in categorized_entries:
        time_of_day_by_magnitude[entry['magnitude_category']][entry['time_of_day']] += 1

    for mag, time_of_day_count in time_of_day_by_magnitude.items():
        time_of_day_labels = time_of_day_count.keys()
        time_of_day_data = time_of_day_count.values()
        create_pie_chart(time_of_day_data, time_of_day_labels, f"Time of Day by {mag} Magnitude", f"time_of_day_by_{mag}.png")

    # 8. Rainfall Category Distribution by Magnitude
    rain_by_magnitude = defaultdict(lambda: defaultdict(int))
    for entry in categorized_entries:
        rain_by_magnitude[entry['magnitude_category']][entry['rain_category']] += 1

    for mag, rain_category_count in rain_by_magnitude.items():
        rain_labels = rain_category_count.keys()
        rain_data = rain_category_count.values()
        create_pie_chart(rain_data, rain_labels, f"Rainfall by {mag} Magnitude", f"rain_by_{mag}.png")

# Main function to load data and create charts
def main(file_path):
    data = load_data(file_path)
    analyze_and_create_charts(data)

# Example usage
if __name__ == "__main__":
    file_path = "merged_data.json"  # Replace with your actual file path
    main(file_path)
