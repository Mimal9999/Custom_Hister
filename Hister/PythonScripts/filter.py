import pandas as pd
import re

# Function to process and filter data from an Excel file
def filter_excel_data(input_excel, output_excel):
    # Reading data from the Excel file
    df = pd.read_excel(input_excel)
    
    # List to store rows for manual verification
    manual_verification = []

    # Function to extract author from title
    def extract_author_from_title(row):
        title = row['Title']
        channel = row['Channel']
        author = row['Author']

        # Check if Author is the same as Channel
        if author == channel:
            # Define patterns to split title
            patterns = [
                r"\s+-\s+", r"-",  # " - " and "-"
                r"\s+:\s+", r":",  # " : " and ":"
            ]

            for pattern in patterns:
                # If a pattern matches, split the title and take the first part
                if re.search(pattern, title):
                    extracted_author = re.split(pattern, title)[0].strip()
                    return extracted_author

            # If no pattern matches, add to manual verification list
            manual_verification.append(row['ID'])
            return author  # Keep the existing author for now
        return author  # If Author != Channel, assume it's correct
    
    # Function to remove author from title
    def remove_author_from_title(title, author):
        # Define patterns to match author followed by separators
        patterns = [
            rf"{re.escape(author)}\s*-\s*",  # "Author -"
            rf"{re.escape(author)}-",       # "Author-"
            rf"{re.escape(author)}\s*:\s*", # "Author :"
            rf"{re.escape(author)}:",       # "Author:"
        ]

        for pattern in patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE).strip()
        return title

    # Definition of the function to select the Author field
    def select_author(row):
        # Extract correct author if possible
        return extract_author_from_title(row)

    # Definition of the function to clean the Title field
    def clean_title(title):
        patterns_to_remove = [
            r' (Official Music Video) ', r' (Official Video) ',
            r'(Explicit)', r'(Tribute Video)', r'(Visualizer)',
            r'Official Audio', r'Music Video', r'(Audio)', r'(Rated R)',
            r'(Official Music Video)', r'(Official Video)', r'(Dirty Version)',
            r'Official Music Video', r'Official Video', r'(Wish Death)', r'Official Lyrics', r"HD UPGRADE",
            r'[\[\]\{\}()"]',
            r'Official'
        ]
        for pattern in patterns_to_remove:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        return title.strip()
    
    # Clean Title and extract correct Author
    df['Filtered Author'] = df.apply(select_author, axis=1)
    df['Filtered Title'] = df['Title'].apply(clean_title)
    
    # Remove author from title
    df['Filtered Title'] = df.apply(
        lambda row: remove_author_from_title(row['Filtered Title'], row['Filtered Author']), axis=1
    )

    # Creating the final DataFrame with selected columns
    filtered_df = df[['ID', 'Filtered Author', 'Filtered Title', 'URL', 'Year', 'Views', 'Name']]
    
    # Renaming columns to final names
    filtered_df.columns = ['ID', 'Author', 'Title', 'URL', 'Year', 'Views', 'Name']
    
    # Saving the results to a new Excel file
    filtered_df.to_excel(output_excel, index=False)
    print(f"The data has been filtered and saved to the file {output_excel}.")

    # Display rows for manual verification
    if manual_verification:
        print(f"Rows requiring manual verification (IDs): {manual_verification}")
    else:
        print("No rows require manual verification.")

# Example usage
input_excel = 'playlist_data.xlsx'  # Path to the input Excel file
output_excel = 'filtered_data.xlsx'  # Path to the output Excel file

# Running the function
filter_excel_data(input_excel, output_excel)
