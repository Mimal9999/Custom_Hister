import pandas as pd
import json

def excel_to_json(excel_file, json_file):
    df = pd.read_excel(excel_file)

    data = df.to_dict(orient='records')

    with open(json_file, 'w', encoding='utf-8') as jsonf:
        json.dump(data, jsonf, ensure_ascii=False, indent=4)

excel_file = 'merged_excel_cleaned.xlsx'
json_file = 'output.json'

excel_to_json(excel_file, json_file)

print(f"Data from file {excel_file} saved to {json_file}.")
