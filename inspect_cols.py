import xlrd, os

# Verifica exatamente o que está nas últimas colunas e o que tem label "TOTAL"
sample = os.path.join(r"C:\dre\Meses", "2025_7_MESANTERIOR.xls")
wb = xlrd.open_workbook(sample)
ws = wb.sheet_by_index(0)
print(f"Colunas: {ws.ncols}")
for col in range(ws.ncols):
    label = ws.cell_value(0, col)
    val1  = ws.cell_value(1, col)
    val2  = ws.cell_value(2, col)
    print(f"  col {col} ({chr(65+col) if col<26 else '??'}): header={repr(label)} | R1={repr(val1)} | R2={repr(val2)}")
