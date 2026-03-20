import pandas as pd
import sys

def analyze_structure():
    file_path = 'todas_filiais.xls'
    try:
        df = pd.read_excel(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    print(f"Columns: {df.columns.tolist()}")
    
    # Analyze the "Descritivo" column
    desc_col = 'Descritivo'
    if desc_col not in df.columns:
        desc_col = df.columns[1] # fallback to second column
    
    print(f"First 100 rows of '{desc_col}':")
    for i, val in enumerate(df[desc_col].head(100)):
        print(f"Row {i:2}: |{val}|")

if __name__ == "__main__":
    analyze_structure()
