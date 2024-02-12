import argparse
import pandas as pd
import re
from collections import Counter
from urllib.request import urlretrieve

def download_file(url, local_filename):
    urlretrieve(url, local_filename)
    return local_filename

def is_image_path(path):
    """Check if the given path is for an image."""
    return bool(re.search(r'\.(jpg|jpeg|gif|png)$', path, re.IGNORECASE))

def identify_browser(user_agent):
    """Identify the browser from a user agent string."""
    if 'Firefox' in user_agent:
        return 'Firefox'
    elif 'MSIE' in user_agent or 'Trident' in user_agent:
        return 'Internet Explorer'
    elif 'Chrome' in user_agent:
        return 'Chrome'
    elif 'Safari' in user_agent and 'Chrome' not in user_agent:
        return 'Safari'
    else:
        return 'Other'

def process_log_file(file_path):
    data = pd.read_csv(file_path, header=None, names=['Path', 'Timestamp', 'UserAgent', 'StatusCode', 'Size'])
    
    # Filter for image hits
    image_hits = data[data['Path'].apply(is_image_path)]
    print(f"Total image hits: {len(image_hits)}")

    # Determine the most popular browser
    browsers = data['UserAgent'].apply(identify_browser)
    browser_counts = Counter(browsers)
    most_popular_browser = browser_counts.most_common(1)[0]
    print(f"Most popular browser: {most_popular_browser[0]} with {most_popular_browser[1]} hits")

    # Optional: Summarize hits by hour
    data['Timestamp'] = pd.to_datetime(data['Timestamp'])
    hits_by_hour = data['Timestamp'].dt.hour.value_counts().sort_index()
    print("Hits by hour:")
    print(hits_by_hour)

def main(url, local_filename='weblog.csv'):
    print(f"Downloading file from {url}...")
    file_path = download_file(url, local_filename)
    print(f"Processing log file: {file_path}")
    process_log_file(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
