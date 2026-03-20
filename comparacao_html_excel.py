"""
Comparação completa HTML (JSON renderizado) vs Excel - linha por linha, valor por valor.
Gera um relatório detalhado de cada linha e cada célula.
"""
import pandas as pd
import json
import re

# Load Excel
df = pd.read_excel('todas_filiais.xls', header=None)
header = [str(c).strip() for c in df.iloc[0].tolist()]
filiais = [h for h in header[2:] if h and h != 'nan']

# Load JSON (same data the HTML uses)
with open('dre.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Flatten JSON hierarchy
json_flat = {}
def flatten(items):
    for item in items:
        name = re.sub(r'\s+', ' ', item['nome'].strip())
        json_flat[name] = item['valores']
        if 'itens' in item:
            flatten(item['itens'])
flatten(data['dados'])

print('=' * 100)
print('COMPARAÇÃO COMPLETA: HTML (via dre.json) vs EXCEL (todas_filiais.xls)')
print('=' * 100)
print(f'Filiais no Excel: {len(filiais)}')
print(f'Filiais no JSON:  {len(data["colunas"])}')
print(f'Linhas no Excel:  {len(df) - 1} (excluindo header)')
print(f'Itens no JSON:    {len(json_flat)}')
print()

total_ok = 0
total_err = 0
total_cells = 0
linhas_ok = 0
linhas_err = 0
faltantes = 0
erros = []

for i in range(1, len(df)):
    row = df.iloc[i]
    desc = str(row[1]).strip()
    if not desc or desc == 'nan':
        continue

    desc_clean = re.sub(r'\s+', ' ', desc)
    linha_num = i + 1

    if desc_clean not in json_flat:
        faltantes += 1
        erros.append(f'LINHA {linha_num} | FALTANTE NO JSON: "{desc_clean}"')
        continue

    json_vals = json_flat[desc_clean]
    linha_ok_flag = True

    for j, filial in enumerate(filiais):
        val_excel = row[j + 2]
        if pd.isna(val_excel):
            val_excel = 0.0
        val_json = json_vals.get(filial, 0.0)
        total_cells += 1
        diff = abs(float(val_excel) - float(val_json))

        if diff > 1e-4:
            total_err += 1
            linha_ok_flag = False
            erros.append(
                f'LINHA {linha_num} | {desc_clean[:45]:45s} | '
                f'{filial[:25]:25s} | Excel={float(val_excel):>14,.2f} | '
                f'JSON={float(val_json):>14,.2f} | Diff={diff:.4f}'
            )
        else:
            total_ok += 1

    if linha_ok_flag:
        linhas_ok += 1
    else:
        linhas_err += 1

# Print results
print('=' * 100)
print('RESULTADO LINHA POR LINHA')
print('=' * 100)
print(f'Linhas 100% corretas:     {linhas_ok}')
print(f'Linhas com divergência:   {linhas_err}')
print(f'Linhas faltantes no JSON: {faltantes}')
print()
print(f'Células comparadas:       {total_cells}')
print(f'Células OK:               {total_ok}')
print(f'Células com erro:         {total_err}')
print()

if erros:
    print('DETALHES DOS ERROS:')
    print('-' * 100)
    for e in erros:
        print(f'  {e}')
else:
    print('✅ RESULTADO FINAL: 100% DE CONFORMIDADE!')
    print('   Todos os valores do HTML/JSON batem perfeitamente com o Excel.')

print()
print('=' * 100)
print('INDICADORES FINANCEIROS - COMPARAÇÃO EXCEL vs JSON')
print('=' * 100)

indicadores_busca = [
    'Total Receita Bruta',
    'Receita Operacional',
    'Margem Bruta',
    'Despesas com pessoal',
    'administrativas',
    'Despesas Operacionais',
    'Lucro Operacional',
    'Resultado antes',
    'Lucro / Prejuizo',
]

total_idx = filiais.index('TOTAL') if 'TOTAL' in filiais else -1

for busca in indicadores_busca:
    for i in range(1, len(df)):
        desc = re.sub(r'\s+', ' ', str(df.iloc[i][1]).strip())
        if busca.lower() in desc.lower():
            if total_idx >= 0:
                val_excel = df.iloc[i][total_idx + 2]
                if pd.isna(val_excel):
                    val_excel = 0.0
                val_json = json_flat.get(desc, {}).get('TOTAL', 0)
                diff = abs(float(val_excel) - float(val_json))
                status = '✅ OK' if diff < 1e-4 else f'❌ DIFF={diff:.2f}'
                print(f'  {desc[:60]:60s} | Excel: R$ {float(val_excel):>14,.2f} | JSON: R$ {float(val_json):>14,.2f} | {status}')
            break

print()
print('=' * 100)
print('COMPARAÇÃO CONCLUÍDA')
print('=' * 100)
