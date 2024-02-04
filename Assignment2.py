import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data."""
    response = urllib.request.urlopen(url)
    data = response.read()
    return data.decode('utf-8')

def processData(file_content):
    """Process the data, converting birthday strings to datetime objects."""
    personData = {}
    lines = file_content.split("\n")
    for i, line in enumerate(lines[1:], start=1):  # Skip the header
        if line:
            try:
                id, name, birthday_str = line.strip().split(',')
                birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y').date()
                personData[int(id)] = (name, birthday)
            except ValueError:
                logging.error(f"Error processing line #{i} for ID #{id}")
    return personData

def displayPerson(id, personData):
    """Display a person's information."""
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print("No user found with that id")

def setup_logging():
    """Set up logging to file."""
    logging.basicConfig(filename='errors.log', level=logging.ERROR, format='%(asctime)s:%(levelname)s:%(message)s')

def main(url):
    """Main function to run the program."""
    setup_logging()
    try:
        csvData = downloadData(url)
        personData = processData(csvData)
    except Exception as e:
        print(f"Failed to download or process data: {e}")
        return
    
    while True:
        user_input = input("Enter an ID to lookup, or 'exit' to quit: ")
        if user_input.lower() == 'exit':
            break
        try:
            id = int(user_input)
            displayPerson(id, personData)
        except ValueError:
            print("Invalid input. Please enter a numeric ID.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
