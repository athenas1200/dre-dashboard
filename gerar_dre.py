import xlrd
import os
import json
import re

# Configurações
MESES_DIR = r"C:\dre\Meses"
OUTPUT_JSON = r"C:\dre\dre.json"
TARGET_MONTH = "fev 2026"  # Mês de referência para o consolidado horizontal

def get_row_type(desc, plano3):
    desc_up = desc.upper()
    if "(=)" in desc_up or re.match(r'^\d+[\.\)]', desc):
        return "categoria"
    if "- ST" in desc_up or "SUB-TOTAL" in desc_up:
        return "st"
    if str(plano3) != "0":
        return "conta"
    return "subcategoria"

def run():
    print(f"Iniciando consolidação dos dados de {MESES_DIR} para {TARGET_MONTH}...")

    # 1. Carregar cadastro de filiais
    filiais_file = os.path.join(MESES_DIR, "filiais.xls")
    if not os.path.exists(filiais_file):
        print("Erro: filiais.xls não encontrado em Meses/")
        return

    wb_f = xlrd.open_workbook(filiais_file)
    ws_f = wb_f.sheet_by_index(0)
    filiais_nomes = {}
    for r in range(1, ws_f.nrows):
        try:
            cod = int(ws_f.cell_value(r, 0))
            nome = ws_f.cell_value(r, 1)
            filiais_nomes[cod] = nome
        except:
            continue

    # 2. Identificar arquivos de dados do mês atual (2026)
    files = [f for f in os.listdir(MESES_DIR) if f.startswith("2026_") and f.endswith(".xls")]
    
    # Mapear dados por filial: { cod_filial: { ordem: valor } }
    dados_consolidados = {}
    colunas_filiais = []

    for fname in files:
        parts = fname.replace(".xls","").split("_")
        cod_filial = int(parts[1])
        
        path = os.path.join(MESES_DIR, fname)
        wb = xlrd.open_workbook(path)
        ws = wb.sheet_by_index(0)
        
        # Localizar a coluna do TARGET_MONTH
        # Header está na linha 0. Colunas de mês são pares (label, valor) a partir da col 2.
        col_idx = -1
        for c in range(2, ws.ncols, 2):
            label = str(ws.cell_value(0, c)).strip().lower()
            if label == TARGET_MONTH:
                col_idx = c + 1 # A coluna de valor é a próxima
                break
        
        if col_idx == -1:
            # print(f"Aviso: Mês {TARGET_MONTH} não encontrado em {fname}")
            continue

        nome_filial = filiais_nomes.get(cod_filial, f"Filial {cod_filial}")
        if nome_filial not in colunas_filiais:
            colunas_filiais.append(nome_filial)
            
        if nome_filial not in dados_consolidados:
            dados_consolidados[nome_filial] = {}
        
        for r in range(1, ws.nrows):
            ordem = str(ws.cell_value(r, 0))
            val = ws.cell_value(r, col_idx)
            try:
                f_val = float(val)
                if abs(f_val - 1e-06) < 1e-08: f_val = 0.0
            except:
                f_val = 0.0
            dados_consolidados[nome_filial][ordem] = f_val

    if not colunas_filiais:
        print(f"Erro: Nenhum dado encontrado para o mês {TARGET_MONTH}")
        return

    colunas_filiais.sort()
    
    # 3. Montar a estrutura hierárquica (usando um arquivo de sample para a estrutura)
    sample_path = os.path.join(MESES_DIR, files[0])
    wb_s = xlrd.open_workbook(sample_path)
    ws_s = wb_s.sheet_by_index(0)
    
    dre_hierarquia = []
    current_cat = None
    current_sub = None
    
    for r in range(1, ws_s.nrows):
        ordem = str(ws_s.cell_value(r, 0))
        desc = str(ws_s.cell_value(r, 1)).strip()
        plano3 = str(ws_s.cell_value(r, 27))
        
        # Calcular valores para esta linha em todas as filiais e o TOTAL
        row_vals = {}
        total_row = 0.0
        for col_name in colunas_filiais:
            val = dados_consolidados.get(col_name, {}).get(ordem, 0.0)
            row_vals[col_name] = round(val, 2)
            total_row += val
        row_vals["TOTAL"] = round(total_row, 2)
        
        tipo = get_row_type(desc, plano3)
        item_data = {
            "nome": desc,
            "valores": row_vals,
            "tipo": tipo,
            "ordem": ordem
        }
        
        if tipo == "categoria":
            current_cat = { **item_data, "itens": [] }
            dre_hierarquia.append(current_cat)
            current_sub = None
        elif tipo == "subcategoria":
            if current_cat:
                current_sub = { **item_data, "itens": [] }
                current_cat["itens"].append(current_sub)
        elif tipo == "st":
            if current_sub:
                current_sub["itens"].append(item_data)
                current_sub = None
            elif current_cat:
                current_cat["itens"].append(item_data)
        else: # conta
            if current_sub:
                current_sub["itens"].append(item_data)
            elif current_cat:
                current_cat["itens"].append(item_data)

    # 4. Gerar JSON
    final_cols = colunas_filiais + ["TOTAL"]
    output = {
        "colunas": final_cols,
        "dados": dre_hierarquia,
        "mes_referencia": TARGET_MONTH
    }
    
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
        
    print(f"Sucesso! {OUTPUT_JSON} gerado com {len(colunas_filiais)} filiais para o mês {TARGET_MONTH}.")

if __name__ == "__main__":
    run()
