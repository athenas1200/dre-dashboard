import json
import pandas as pd

with open('dre.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print('=== ESTRUTURA DO DRE ===')
print('Total de colunas (filiais):', len(data['colunas']))
for c in data['colunas']:
    print('  -', c)

print('\n=== CATEGORIAS PRINCIPAIS ===')
for i, cat in enumerate(data['dados']):
    total = cat['valores'].get('TOTAL', 0)
    def count_all(items):
        c = 0
        for it in items:
            c += 1
            if 'itens' in it:
                c += count_all(it['itens'])
        return c
    total_itens = count_all(cat.get('itens', []))
    print(f'{i+1:2}. {cat["nome"][:65]:65s} | TOTAL: R$ {total:>15,.2f} | Tipo: {cat["tipo"]:12s} | Itens: {total_itens}')

print('\n=== VERIFICACAO: TOTAL vs SOMA FILIAIS ===')
erros_total = 0
# Check all items recursively
def check_totals(items, path=""):
    global erros_total
    for item in items:
        total_val = item['valores'].get('TOTAL', 0)
        soma = sum(v for k, v in item['valores'].items() 
                   if k != 'TOTAL' and k != '99-Rommatian Escritório 14º andar  MS')
        diff = abs(total_val - soma)
        if diff > 0.1 and abs(total_val) > 1:
            print(f'  DIVERGENCIA: {path}{item["nome"][:50]:50s} | TOTAL={total_val:>12,.2f} | Soma={soma:>12,.2f} | Diff={diff:.4f}')
            erros_total += 1
        if 'itens' in item:
            check_totals(item['itens'], path + "  ")

check_totals(data['dados'])
if erros_total == 0:
    print('  OK: Nenhuma divergencia TOTAL vs Soma encontrada')
else:
    print(f'  ATENCAO: {erros_total} divergencias encontradas')

# Check placeholder values
print('\n=== VERIFICACAO: VALORES PLACEHOLDER (1e-06) ===')
placeholder_count = 0
total_valores = 0
def count_placeholders(items):
    global placeholder_count, total_valores
    for item in items:
        for k, v in item['valores'].items():
            total_valores += 1
            if v == 1e-06:
                placeholder_count += 1
        if 'itens' in item:
            count_placeholders(item['itens'])

count_placeholders(data['dados'])
print(f'  Total de celulas de valor: {total_valores}')
print(f'  Valores 1e-06 (placeholder zero): {placeholder_count}')
print(f'  Percentual placeholder: {placeholder_count/total_valores*100:.1f}%')

# Check hierarchy integrity 
print('\n=== VERIFICACAO: HIERARQUIA ===')
cats_sem_itens = 0
subs_sem_itens = 0
for cat in data['dados']:
    if len(cat.get('itens', [])) == 0 and cat['tipo'] == 'categoria':
        cats_sem_itens += 1
    for item in cat.get('itens', []):
        if item.get('tipo') == 'subcategoria' and len(item.get('itens', [])) == 0:
            subs_sem_itens += 1
            print(f'  AVISO: Subcategoria vazia: {item["nome"]}')

print(f'  Categorias sem itens: {cats_sem_itens}')
print(f'  Subcategorias vazias: {subs_sem_itens}')

# Financial summary
print('\n=== RESUMO FINANCEIRO (coluna TOTAL) ===')
for cat in data['dados']:
    total = cat['valores'].get('TOTAL', 0)
    if abs(total) > 0.01:
        sinal = '+' if total > 0 else '-'
        print(f'  {cat["nome"][:60]:60s} => R$ {total:>15,.2f}')
    elif cat['tipo'] == 'resultado':
        print(f'  {cat["nome"][:60]:60s} => R$ {total:>15,.2f}  [ZERADO]')

# Cross-validate with Excel
print('\n=== CROSS-VALIDACAO COM EXCEL ===')
df = pd.read_excel('todas_filiais.xls', header=None)
print(f'  Linhas no Excel: {len(df)}')
print(f'  Colunas no Excel: {len(df.columns)}')
header = [str(c).strip() for c in df.iloc[0].tolist()]
print(f'  Header Excel: {header[:5]}...')

excel_rows_with_data = 0
for i in range(1, len(df)):
    desc = str(df.iloc[i][1]).strip()
    if desc and desc != 'nan':
        excel_rows_with_data += 1

json_flat_count = 0
def count_json_items(items):
    global json_flat_count
    for item in items:
        json_flat_count += 1
        if 'itens' in item:
            count_json_items(item['itens'])

count_json_items(data['dados'])
print(f'  Linhas com dados no Excel: {excel_rows_with_data}')
print(f'  Itens totais no JSON: {json_flat_count}')
if excel_rows_with_data == json_flat_count:
    print('  OK: Contagem Excel == Contagem JSON')
else:
    print(f'  DIVERGENCIA: Excel={excel_rows_with_data} vs JSON={json_flat_count}')

print('\n=== ANALISE CONCLUIDA ===')
