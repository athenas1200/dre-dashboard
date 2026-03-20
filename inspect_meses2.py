import xlrd
import os
import re

meses_dir = r"C:\dre\Meses"
files = sorted(os.listdir(meses_dir))

# Carrega filiais.xls
wb_f = xlrd.open_workbook(os.path.join(meses_dir, "filiais.xls"))
ws_f = wb_f.sheet_by_index(0)
filiais = {}
for row in range(1, ws_f.nrows):
    cod = int(ws_f.cell_value(row, 0))
    nome = ws_f.cell_value(row, 1)
    filiais[cod] = nome

print("=== FILIAIS CADASTRADAS ===")
for k, v in sorted(filiais.items()):
    print(f"  {k}: {v}")

print("\n=== ARQUIVOS POR TIPO ===")
atuais = [f for f in files if "MESATUAL" in f]
anteriores = [f for f in files if "MESANTERIOR" in f]
print(f"MESATUAL: {len(atuais)} arquivos")
print(f"MESANTERIOR: {len(anteriores)} arquivos")

# Extrai estrutura de um arquivo e mostra quais meses tem dados
print("\n=== ESTRUTURA COLUNAS (MESANTERIOR 2025 filial 12) ===")
sample = os.path.join(meses_dir, "2025_12_MESANTERIOR.xls")
wb = xlrd.open_workbook(sample)
ws = wb.sheet_by_index(0)
# Pega os cabeçalhos de mês (colunas pares: C=2, E=4, G=6... até Y=24)
# Padrão: col_par = MÊS label, col_ímpar seguinte = VALOR
month_cols = []
for col in range(2, ws.ncols-2, 2):  # pulando últimas 2 (Filial, Plano3)
    label = ws.cell_value(0, col)
    if label and label != '-':
        month_cols.append((col, label))
        
print("Colunas de meses disponíveis:")
for col, label in month_cols:
    # Pega um valor não-zero para ver se tem dados
    has_data = any(ws.cell_value(r, col+1) not in (0.0, 1e-06, '') for r in range(1, ws.nrows))
    print(f"  Col {col}({chr(65+col)})+{col+1}({chr(65+col+1)}): '{label}' | tem dados: {has_data}")

# Checar col 26 e 27 (Filial, Plano3)
print(f"\n  Col 26 = Filial: primeiros valores = {[ws.cell_value(r, 26) for r in range(1,5)]}")
print(f"  Col 27 = Plano3: primeiros valores = {[ws.cell_value(r, 27) for r in range(1,5)]}")

# Pegar todas as linhas únicas (estrutura DRE)
print("\n=== LINHAS DRE (primeiras 30) ===")
for row in range(1, min(30, ws.nrows)):
    ordem = ws.cell_value(row, 0)
    desc = ws.cell_value(row, 1)
    plano = ws.cell_value(row, 27)
    print(f"  Ordem={ordem} | Plano3={plano} | Desc='{desc}'")
