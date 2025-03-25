import requests
import os
from dotenv import load_dotenv

# Load environment variables from ..env file
load_dotenv()

# Access the API key from the environment variables
API_KEY = os.getenv('API_KEY')

def fetch_data(animal_name):
    """
    Fetches the animals data for the animal 'animal_name' from the API.

    Args:
        animal_name (str): The name of the animal to search for.

    Returns:
        list: A list of animals, each animal is a dictionary, or an empty list
              if there was an error or no data found. The dictionary format is:
              {
                'name': ...,
                'taxonomy': {
                  ...
                },
                'locations': [
                  ...
                ],
                'characteristics': {
                  ...
                }
              }
    """

    if not API_KEY:
        print("Error: API_KEY not found in environment variables.  Please set the API_KEY environment variable.")
        return []  # Return an empty list if the API key is missing

    api_url = f"https://api.api-ninjas.com/v1/animals?name={animal_name}"
    headers = {'X-Api-Key': API_KEY}
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()  # Returns the API response (list of dictionaries)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from API: {e}")
        return []  # Returns empty list if error

if __name__ == '__main__':
    # Example usage (optional - you can remove this)
    animal_name = "Fox"
    animal_data = fetch_data(animal_name)

    if animal_data:
        print(f"Data for {animal_name}:")
        print(animal_data)  # Print the entire response for inspection
    else:
        print(f"Could not retrieve data for {animal_name}.")