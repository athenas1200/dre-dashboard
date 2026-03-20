import xlrd, os, json

def audit_meses():
    json_path = r"C:\dre\dre_meses.json"
    meses_dir = r"C:\dre\Meses"
    
    if not os.path.exists(json_path):
        print(f"ERRO: {json_path} não encontrado.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data_json = json.load(f)
    
    files = sorted([f for f in os.listdir(meses_dir) if f.endswith(".xls") and f != "filiais.xls"])
    total_files = len(files)
    total_cells = 0
    divergences = []
    
    print(f"Iniciando Auditoria Mestre em {total_files} arquivos...")
    
    for fname in files:
        parts = fname.replace(".xls","").split("_")
        ano  = parts[0]
        cod  = parts[1]
        tipo = "atual" if "MESATUAL" in fname else "anterior"
        
        filepath = os.path.join(meses_dir, fname)
        wb = xlrd.open_workbook(filepath)
        ws = wb.sheet_by_index(0)
        
        # Mapeia colunas de meses no XLS
        meses_xls = []
        for col in range(2, ws.ncols-1, 2):
            label = str(ws.cell_value(0, col)).strip().lower()
            if not label or label == '-' or not any(m in label for m in ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']):
                continue
            meses_xls.append((col, label))
            
        for col, label in meses_xls:
            for row in range(1, ws.nrows):
                ordem = str(ws.cell_value(row, 0))
                val_xls = ws.cell_value(row, col+1)
                
                # Tratamento de valor igual ao script de geração
                try:
                    vf_xls = float(val_xls)
                    # Arredonda para 2 casas (padrão financeiro)
                    if abs(vf_xls - 1e-06) < 1e-10:
                        vf_xls = 0.0
                    else:
                        vf_xls = round(vf_xls, 2)
                except (TypeError, ValueError):
                    vf_xls = 0.0
                
                # Pega valor do JSON (já está arredondado no gerar_dre_meses.py)
                val_json = data_json["dados"].get(cod, {}).get(tipo, {}).get(label, {}).get(ordem, 0.0)
                
                total_cells += 1
                if abs(vf_xls - val_json) > 0.0001:
                    divergences.append({
                        "arquivo": fname,
                        "filial": cod,
                        "mes": label,
                        "ordem": ordem,
                        "xls": vf_xls,
                        "json": val_json
                    })

    print("-" * 50)
    print(f"Arquivos conferidos: {total_files}")
    print(f"Células conferidas:  {total_cells}")
    print(f"Divergências:        {len(divergences)}")
    print("-" * 50)
    
    if len(divergences) > 0:
        print("DETALHES DAS DIVERGÊNCIAS:")
        for d in divergences[:20]: # limita exibição
            print(f"  Filial {d['filial']} | {d['mes']} | Ordem {d['ordem']}: XLS={d['xls']} vs JSON={d['json']}")
        if len(divergences) > 20:
            print(f"  ... e mais {len(divergences)-20} erros.")
        
        # Salva log de erros
        with open(r"C:\dre\auditoria_meses_erros.json", "w", encoding="utf-8") as f:
            json.dump(divergences, f, indent=2)
    else:
        print("CONFORMIDADE 100%! Todos os dados do Excel batem com o Dashboard.")

if __name__ == "__main__":
    audit_meses()
