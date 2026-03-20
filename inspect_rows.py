import pandas as pd

def inspect_rows():
    df = pd.read_excel('todas_filiais.xls', header=None)
    # Print rows 20 to 35 (approx Despesas com pessoal)
    print("Rows 20 to 50:")
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)
    print(df.iloc[20:51, :5]) # Show first 5 columns

if __name__ == "__main__":
    inspect_rows()
