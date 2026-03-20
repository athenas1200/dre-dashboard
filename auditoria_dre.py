import pandas as pd
import json
import os
import re

def run_audit():
    excel_file = "todas_filiais.xls"
    json_file = "dre.json"
    
    if not os.path.exists(excel_file) or not os.path.exists(json_file):
        print("Erro: Arquivos não encontrados.")
        return

    print("=== AUDITORIA PROFISSIONAL: LINHA POR LINHA ===")
    
    df_excel = pd.read_excel(excel_file, header=None)
    header_excel = [str(c).strip() for c in df_excel.iloc[0].tolist()]
    filiais_excel = header_excel[2:]
    
    with open(json_file, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
    
    # Mapear JSON para flat por nome exato
    json_flat = {}
    def flatten(items):
        for item in items:
            name = item['nome'].strip()
            name = re.sub(r'\s+', ' ', name)
            json_flat[name] = item['valores']
            if 'itens' in item:
                flatten(item['itens'])
    
    flatten(data_json['dados'])
    
    errors = 0
    missing = 0
    total_checks = 0
    
    for i in range(1, len(df_excel)):
        row = df_excel.iloc[i]
        desc = str(row[1]).strip()
        if not desc or desc == 'nan': continue
        
        desc_clean = re.sub(r'\s+', ' ', desc)
        
        if desc_clean not in json_flat:
            print(f"ERRO: LINHA {i+1} - Nome '{desc_clean}' não encontrado no JSON.")
            missing += 1
            continue
            
        json_vals = json_flat[desc_clean]
        for j, filial in enumerate(filiais_excel):
            val_excel = row[j+2]
            if pd.isna(val_excel): val_excel = 0.0
            val_json = json_vals.get(filial, 0.0)
            
            diff = abs(float(val_excel) - float(val_json))
            total_checks += 1
            if diff > 1e-4:
                print(f"ERRO: LINHA {i+1} | {desc_clean} | Filial: {filial} | Excel: {val_excel} | JSON: {val_json} | Diff: {diff}")
                errors += 1

    print("\n=== RESULTADO FINAL ===")
    print(f"Linhas validadas com sucesso: { (len(df_excel)-1) - missing }")
    print(f"Células conferidas: {total_checks}")
    print(f"Discrepâncias de valores: {errors}")
    print(f"Itens faltantes: {missing}")
    
    if errors == 0 and missing == 0:
        print("\nAUDITORIA CONCLUIDA COM SUCESSO: 100% de conformidade tecnica e financeira.")
    else:
        print("\nAUDITORIA REPROVADA: Verifique os erros acima.")

if __name__ == "__main__":
    run_audit()
