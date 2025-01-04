import pandas as pd
import re

# Function to process and filter data from an Excel file
def filter_excel_data(input_excel, output_excel):
    # Reading data from the Excel file
    df = pd.read_excel(input_excel)
    
    # Definition of the function to select the Author field
    def select_author(row):
        if row['Artist'] != 'No Data':
            return row['Artist']
        elif row['Author'] != 'No Data':
            return row['Author']
        else:
            return row['Channel']
    
    # Definition of the function to select the Title field
    def select_title(row):
        if row['Track Title'] != 'No Data':
            return row['Track Title']
        else:
            return row['Title']
    
    # Definition of the function to clean the Title field
    def clean_title(title):
        # Removing unnecessary fragments and characters
        patterns_to_remove = [
            r' (Official Music Video) ', r' (Official Video) ',
            r'(Explicit)', r'(Tribute Video)', r'(Visualizer)',
            r'Official Audio', r'Music Video', r'(Audio)', r'(Rated R)',
            r'(Official Music Video)', r'(Official Video)', r'(Dirty Version)',
            r'Official Music Video', r'Official Video', r'(Wish Death)', r'Official Lyrics',
            r'[\[\]\{\}"-]',
            r'Official'
        ]
        for pattern in patterns_to_remove:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        return title.strip()
    
    # Definition of the function to remove the author's name from the Title
    def remove_author_from_title(title, author):
        if pd.notna(author):
            title = re.sub(r'\b' + re.escape(author) + r'\b', '', title, flags=re.IGNORECASE)
        return title.strip()
    
    # Definition of the function to clean up duplicate spaces and remove empty brackets
    def clean_up_spaces_and_brackets(title):
        # Removing () characters and extra spaces
        title = re.sub(r'\(\s*\)', '', title)  # Removing empty brackets
        title = re.sub(r'\s+', ' ', title)  # Removing duplicate spaces
        title = title.strip()  # Removing spaces at the beginning and end
        return title

    # Definition of the function to remove spaces before ')' and after '('
    def remove_spaces_around_brackets(title):
        # Removing spaces before the closing bracket ')'
        title = re.sub(r'\s+\)', ')', title)
        # Removing spaces after the opening bracket '('
        title = re.sub(r'\(\s+', '(', title)
        title = re.sub(r'^\s*[,|-]\s*', '', title)
        title = re.sub(r'–', '', title)

        return title
    
    # Creating new columns with selected and processed data
    df['Filtered Author'] = df.apply(select_author, axis=1)
    df['Filtered Title'] = df.apply(select_title, axis=1).apply(clean_title)
    df['Filtered Title'] = df.apply(lambda row: remove_author_from_title(row['Filtered Title'], row['Filtered Author']), axis=1)
    
    # Second filtering - cleaning up brackets and duplicate spaces
    df['Filtered Title'] = df['Filtered Title'].apply(clean_up_spaces_and_brackets)
    
    # Third filtering - removing spaces before ')' and after '('
    df['Filtered Title'] = df['Filtered Title'].apply(remove_spaces_around_brackets)
    
    # Creating the final DataFrame with selected columns
    filtered_df = df[['ID', 'Filtered Author', 'Filtered Title', 'URL', 'Year', 'Views', 'Name']]
    
    # Renaming columns to final names
    filtered_df.columns = ['ID', 'Author', 'Title', 'URL', 'Year', 'Views', 'Name']
    
    # Saving the results to a new Excel file
    filtered_df.to_excel(output_excel, index=False)
    print(f"The data has been filtered and saved to the file {output_excel}.")

# Example usage
input_excel = 'playlist_data.xlsx'  # Path to the input Excel file
output_excel = 'filtered_data.xlsx'  # Path to the output Excel file

# Running the function
filter_excel_data(input_excel, output_excel)
