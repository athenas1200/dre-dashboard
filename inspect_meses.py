import xlrd
import os

def inspect_xls(filepath, max_rows=5):
    wb = xlrd.open_workbook(filepath)
    ws = wb.sheet_by_index(0)
    print(f"\n=== {os.path.basename(filepath)} ===")
    print(f"Sheets: {wb.sheet_names()}")
    print(f"Rows: {ws.nrows}, Cols: {ws.ncols}")
    print("\nRow 0 (headers):")
    for col in range(ws.ncols):
        val = ws.cell_value(0, col)
        print(f"  Col {col} ({chr(65+col)}): {repr(val)}")
    print(f"\nFirst {max_rows} rows of data:")
    for row in range(1, min(max_rows+1, ws.nrows)):
        row_vals = [ws.cell_value(row, col) for col in range(ws.ncols)]
        print(f"  Row {row}: {row_vals}")

# Inspeciona filiais.xls
inspect_xls(r"C:\dre\Meses\filiais.xls", max_rows=10)

# Pega um arquivo de MesAtual e um de MesAnterior para comparar
meses_dir = r"C:\dre\Meses"
files = os.listdir(meses_dir)
atual = next(f for f in files if "MESATUAL" in f)
anterior = next(f for f in files if "MESANTERIOR" in f)

inspect_xls(os.path.join(meses_dir, atual), max_rows=5)
inspect_xls(os.path.join(meses_dir, anterior), max_rows=5)
