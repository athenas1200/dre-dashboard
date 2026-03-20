import json
with open(r'C:\dre\auditoria_meses_erros.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

max_err = 0
for d in data:
    err = abs(d['xls'] - d['json'])
    if err > max_err:
        max_err = err
    if err > 0.01:
        print(f"Erro > 0.01: Filial {d['id_filial'] if 'id_filial' in d else d.get('filial')} | {d['mes']} | Ordem {d['ordem']}: XLS={d['xls']} vs JSON={d['json']} (diff={err})")

print(f"Erro máximo encontrado: {max_err}")
print(f"Total de erros: {len(data)}")
