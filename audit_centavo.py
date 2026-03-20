import xlrd
import os
import json

def audit():
    meses_dir = r"C:\dre\Meses"
    json_path = r"C:\dre\dre_meses.json"
    
    if not os.path.exists(json_path):
        print(f"ERRO: {json_path} não encontrado.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    files = [f for f in os.listdir(meses_dir) if f.endswith(".xls") and f != "filiais.xls"]
    
    discrepancies = []
    total_checks = 0

    print(f"Iniciando auditoria de {len(files)} arquivos...")

    for fname in files:
        parts = fname.replace(".xls","").split("_")
        ano = parts[0]
        cod = parts[1] # JSON uses string keys for filiais
        tipo = "atual" if "MESATUAL" in fname else "anterior"
        
        wb = xlrd.open_workbook(os.path.join(meses_dir, fname))
        ws = wb.sheet_by_index(0)
        
        # Discover month columns (same as gerar_dre_meses.py)
        meses_encontrados = []
        for col in range(2, ws.ncols-1, 2):
            label = str(ws.cell_value(0, col)).strip().lower()
            if not label or label == '-' or not any(m in label for m in ['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez']):
                continue
            meses_encontrados.append((col, label))

        for col, label in meses_encontrados:
            for row in range(1, ws.nrows):
                ordem = str(ws.cell_value(row, 0))
                val_xls = ws.cell_value(row, col+1)
                
                try:
                    val_xls = float(val_xls)
                    if abs(val_xls - 1e-06) < 1e-10:
                        val_xls = 0.0
                except:
                    val_xls = 0.0
                
                val_xls = round(val_xls, 2)
                
                # Check against JSON
                val_json = data['dados'].get(cod, {}).get(tipo, {}).get(label, {}).get(ordem, 0.0)
                
                total_checks += 1
                if abs(val_xls - val_json) > 0.001:
                    discrepancies.append({
                        "file": fname,
                        "month": label,
                        "ordem": ordem,
                        "xls": val_xls,
                        "json": val_json
                    })

    print(f"\nAuditoria Finalizada.")
    print(f"Total de pontos verificados: {total_checks}")
    if not discrepancies:
        print("RESULTADO: 100% DE ACURACIDADE (Nenhuma divergência encontrada).")
    else:
        print(f"RESULTADO: {len(discrepancies)} DIVERGÊNCIAS ENCONTRADAS!")
        for d in discrepancies[:10]:
            print(f"  - {d['file']} | {d['month']} | ID {d['ordem']}: XLS={d['xls']}, JSON={d['json']}")
        if len(discrepancies) > 10:
            print(f"  ... e mais {len(discrepancies)-10} erros.")

if __name__ == "__main__":
    audit()
