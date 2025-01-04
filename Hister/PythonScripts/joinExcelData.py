import pandas as pd
import os

# Funkcja do łączenia plików Excel w jeden DataFrame
def append(path):
    # Tworzenie pustej listy do przechowywania DataFrame'ów
    frames = []    
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.xlsx'):  # Tylko pliki .xlsx
                file_with_path = os.path.join(root, file)          
                df = pd.read_excel(file_with_path)      
                frames.append(df)
    df = pd.concat(frames, axis=0, ignore_index=True)    
    return df

# Funkcja do usuwania pierwszej kolumny, która nie ma nazwy
def remove_empty_column(df):
    # Sprawdzenie, czy pierwsza kolumna ma pustą nazwę
    if df.columns[0] == '' or pd.isna(df.columns[0]):
        df = df.drop(df.columns[0], axis=1)  # Usunięcie pierwszej kolumny
    return df

# Funkcja do usuwania duplikatów w kolumnie 'URL'
def remove_duplicates_by_url(df):
    df = df.drop_duplicates(subset='URL', keep='first')  # Usunięcie duplikatów na podstawie kolumny 'URL'
    return df

# Ścieżka do folderu z plikami Excel
path = "ExcelFiles"

# Łączenie danych z plików Excel
df = append(path)

# Usunięcie pierwszej kolumny, która nie ma nazwy
df = remove_empty_column(df)

# Usunięcie powtarzających się wystąpień w kolumnie 'URL'
df = remove_duplicates_by_url(df)

# Zapisanie wynikowego DataFrame do pliku Excel
df.to_excel("merged_excel_cleaned.xlsx", index=False)

print("Połączono pliki i zapisano dane do pliku 'merged_excel_cleaned.xlsx'.")
