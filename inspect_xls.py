import pandas as pd
import sys

def inspect_xls(filename):
    try:
        # Try to read the file. Note: .xls requires 'xlrd'
        # If xlrd is not installed, this might fail.
        df = pd.read_excel(filename)
        print("Headers:")
        print(df.columns.tolist())
        print("\nPrimeiras 10 linhas:")
        print(df.head(10).to_string())
        
        # Also check for sheets
        xls = pd.ExcelFile(filename)
        print("\nPlanilhas encontradas:")
        print(xls.sheet_names)
        
    except Exception as e:
        print(f"Erro: {e}")
        if "xlrd" in str(e):
            print("\nSugestão: Instalar 'xlrd' para ler arquivos .xls")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_xls(sys.argv[1])
    else:
        inspect_xls("todas_filiais.xls")
