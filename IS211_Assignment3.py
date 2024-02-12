import csv
import re
from collections import Counter
from datetime import datetime

# Function to process the CSV file and return its data
def process_file(filename):
    data = []
    with open(filename, newline='') as csvfile:
        logreader = csv.reader(csvfile)
        for row in logreader:
            data.append(row)
    return data

# Function to calculate and print the percentage of image requests
def calculate_image_stats(data):
    total_hits = len(data)
    image_hits = sum(1 for row in data if re.search(r'\.(jpg|gif|png|JPG|GIF|PNG)$', row[0]))
    image_percentage = (image_hits / total_hits) * 100 if total_hits > 0 else 0
    print(f"Image requests account for {image_percentage:.2f}% of all requests")

# Function to determine and print the most popular browser
def find_most_popular_browser(data):
    browser_counts = Counter()
    browsers = ['Firefox', 'Chrome', 'Internet Explorer', 'Safari']
    
    for row in data:
        user_agent = row[2]
        for browser in browsers:
            if browser in user_agent:
                browser_counts[browser] += 1
                break

    most_common_browser, count = browser_counts.most_common(1)[0]
    print(f"The most popular browser is {most_common_browser} with {count} hits")

# Function to calculate and print the number of hits per hour
def hits_per_hour(data):
    hour_counts = Counter(datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S').hour for row in data)
    
    for hour in range(24):
        print(f"Hour {hour:02d} has {hour_counts[hour]} hits")

# Main execution function
def main():
    # Replace 'weblog.csv' with your actual log file path
    file_path = 'weblog (1).csv'
    data = process_file(file_path)
    
    print("\nCalculating image statistics...")
    calculate_image_stats(data)
    
    print("\nDetermining the most popular browser...")
    find_most_popular_browser(data)
    
    print("\nCalculating hits per hour (Extra Credit)...")
    hits_per_hour(data)

if __name__ == '__main__':
    main()
