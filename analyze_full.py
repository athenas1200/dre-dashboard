import pandas as pd

def analyze_full(filename):
    try:
        df = pd.read_excel(filename, header=None) # Read without headers to see everything
        print("First 50 rows (Full Structure):")
        # Display index and content
        for i, row in df.head(50).iterrows():
            print(f"Row {i}: {row.tolist()[:10]}") # Only first 10 columns for brevity
            
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    analyze_full("todas_filiais.xls")
