import xlrd, os, json

meses_dir = r"C:\dre\Meses"

# Carrega filiais
wb_f = xlrd.open_workbook(os.path.join(meses_dir, "filiais.xls"))
ws_f = wb_f.sheet_by_index(0)
filiais = {}
for row in range(1, ws_f.nrows):
    cod = int(ws_f.cell_value(row, 0))
    nome = str(ws_f.cell_value(row, 1)).replace("Rommanel ", "").replace("ROMMANEL ", "").strip()
    filiais[cod] = nome

# Pega estrutura DRE completa de um arquivo
sample = os.path.join(meses_dir, "2025_12_MESANTERIOR.xls")
wb = xlrd.open_workbook(sample)
ws = wb.sheet_by_index(0)

estrutura = []
for row in range(1, ws.nrows):
    ordem = ws.cell_value(row, 0)
    desc  = ws.cell_value(row, 1)
    plano = ws.cell_value(row, 27)
    estrutura.append({"ordem": str(ordem), "descritivo": desc, "plano3": str(plano)})

print(f"Total linhas DRE: {len(estrutura)}")
print(json.dumps(estrutura[:10], ensure_ascii=False, indent=2))

# Mapeia todos os arquivos disponíveis
files = sorted([f for f in os.listdir(meses_dir) if f.endswith(".xls") and f != "filiais.xls"])
print(f"\nTotal arquivos de filiais: {len(files)}")

# Extrai todos os dados por filial e mês
dados = {}  # dados[cod_filial][tipo_mes][mes_label][ordem] = valor

for fname in files:
    parts = fname.replace(".xls","").split("_")
    ano  = parts[0]
    cod  = int(parts[1])
    tipo = "atual" if "MESATUAL" in fname else "anterior"
    
    wb2 = xlrd.open_workbook(os.path.join(meses_dir, fname))
    ws2 = wb2.sheet_by_index(0)
    
    if cod not in dados:
        dados[cod] = {"atual": {}, "anterior": {}}
    
    # Descobre colunas de mês (pares label+valor: cols 2,3 / 4,5 / ...)
    meses_encontrados = []
    for col in range(2, ws2.ncols-1, 2):
        label = str(ws2.cell_value(0, col)).strip().lower()
        # Valida se o label parece um mês (ex: "jan 2025")
        if not label or label == '-' or not any(m in label for m in ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']):
            continue
        
        meses_encontrados.append((col, label))

    for col, label in meses_encontrados:
        if label not in dados[cod][tipo]:
            dados[cod][tipo][label] = {}
        for row in range(1, ws2.nrows):
            ordem = str(ws2.cell_value(row, 0))
            val   = ws2.cell_value(row, col+1)
            # Converte para float e ignora marcadores (1e-06 = sem dado real)
            try:
                val = float(val)
                if abs(val - 1e-06) < 1e-10:
                    val = 0.0
            except (TypeError, ValueError):
                val = 0.0
            dados[cod][tipo][label][ordem] = round(val, 2)

# Garante que todas as filiais tenham os 12 meses de 2025 e 2026 (mesmo que zerados)
meses_nomes = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
for cod in dados:
    for mes_nome in meses_nomes:
        label_2025 = f"{mes_nome} 2025"
        label_2026 = f"{mes_nome} 2026"
        if label_2025 not in dados[cod]["anterior"]:
            dados[cod]["anterior"][label_2025] = {str(item["ordem"]): 0.0 for item in estrutura}
        if label_2026 not in dados[cod]["atual"]:
            dados[cod]["atual"][label_2026] = {str(item["ordem"]): 0.0 for item in estrutura}

# Monta JSON final
output = {
    "filiais": filiais,
    "estrutura_dre": estrutura,
    "dados": {str(k): v for k, v in dados.items()}
}

with open(r"C:\dre\dre_meses.json", "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\nFiliais com dados: {list(dados.keys())}")
# Mostra meses disponíveis de uma filial
sample_cod = 12
print(f"\nFilial {sample_cod} - meses anterior: {sorted(dados[sample_cod]['anterior'].keys())}")
print(f"Filial {sample_cod} - meses atual: {sorted(dados[sample_cod]['atual'].keys())}")
print(f"\ndre_meses.json gerado com sucesso!")
