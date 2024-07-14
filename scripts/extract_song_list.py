import os
import re
import pandas as pd
import unicodedata

def extract_info_from_sbx(file_path, lang, part):
    data = []

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

        entries = re.findall(r'\\idxentry\{(.+?)\\\s*--\s*\\normalsize\s*(.+?)}', content)

        for entry in entries:
            name, author = entry

            data.append({
                'název': name,
                'autor': author,
                'jazyk': lang,
                'část': part
            })

    return pd.DataFrame(data)

def process_sbx_files(directory):
    all_data = pd.DataFrame()

    for lang in "czech", "international":
        for part in "1", "2":
            filename = f"idx{part}{lang}.sbx"
            file_path = os.path.join(directory, filename)
            file_data = extract_info_from_sbx(file_path, lang, part)
            all_data = pd.concat([all_data, file_data], ignore_index=True)

    return all_data

# Replace 'your_directory_path' with the path to your directory containing *.sbx files
directory_path = './toc'
result_dataframe = process_sbx_files(directory_path)

# Sort the dataframe by 'jazyk' and 'jméno' columns, consider unicode characters
result_dataframe = result_dataframe.sort_values(by=['jazyk', 'název'], key=lambda col: col.str.normalize('NFKD'))

# Replace all \& with &
result_dataframe = result_dataframe.replace(r'\\&', '&', regex=True)


# Display the resulting Pandas dataframe
print(result_dataframe)

result_dataframe.to_csv('song_list.csv', index=False)
result_dataframe.to_excel('song_list.xlsx', index=False)
