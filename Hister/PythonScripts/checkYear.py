import pandas as pd
import requests
import time

# Function to query MusicBrainz API
def query_musicbrainz(author, title):
    base_url = "https://musicbrainz.org/ws/2/recording/"
    params = {
        "query": f'artist:"{author}" AND recording:"{title}"',
        "fmt": "json",
        "limit": 100
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error querying MusicBrainz API for {author} - {title}: {e}")
        return None

# Function to find the earliest year from MusicBrainz data
def get_earliest_year(data, original_year):
    if not data or "recordings" not in data:
        return original_year  # Return the original year if no data is available

    earliest_year = original_year  # Default to original year
    for recording in data["recordings"]:
        # Extract the release date if available
        if "first-release-date" in recording:
            try:
                year = int(recording["first-release-date"][:4])  # Extract the year
                if year < earliest_year:  # Update earliest year
                    earliest_year = year
            except ValueError:
                continue  # Skip invalid dates
    return earliest_year

# Main function to process the Excel file
def verify_and_update_years(input_excel, output_excel):
    # Load the data
    df = pd.read_excel(input_excel)

    # List to store IDs of rows where Year was updated
    updated_ids = []

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        author = row["Author"]
        title = row["Title"]
        original_year = row["Year"]

        # Query MusicBrainz API for the author and title
        print(f"Querying MusicBrainz for: {author} - {title}")
        data = query_musicbrainz(author, title)

        # Get the earliest year from the API response
        earliest_year = get_earliest_year(data, original_year)

        # Update the Year column if the earliest year is earlier
        if earliest_year < original_year:
            print(f"Updating Year for '{title}' by {author}: {original_year} -> {earliest_year}")
            df.at[index, "Year"] = earliest_year
            updated_ids.append(row["ID"])  # Store the ID of the updated row

        # Pause to respect API rate limits
        time.sleep(1)  # Sleep for 1 second between requests

    # Save the updated DataFrame to a new Excel file
    df.to_excel(output_excel, index=False)
    print(f"The updated data has been saved to {output_excel}")

    # Print all IDs where Year was updated
    if updated_ids:
        print(f"Year was updated for {len(updated_ids)} rows. IDs: {', '.join(map(str, updated_ids))}")
    else:
        print("No changes were made to the Year column.")

# Example usage
input_excel = "filtered_data.xlsx"  # Input file from previous script
output_excel = "verified_data.xlsx"  # Output file with verified years

# Run the verification function
verify_and_update_years(input_excel, output_excel)
