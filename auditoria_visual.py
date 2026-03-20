import json
from playwright.sync_api import sync_playwright

def test_visual_html():
    with open(r'c:\dre\dre_meses.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    expected_total_13 = 0.0
    for filial, fil_data in data['dados'].items():
        val = fil_data.get('atual', {}).get('fev 2026', {}).get('13', 0.0)
        expected_total_13 += val

    expected_total_173 = 0.0
    for filial, fil_data in data['dados'].items():
        val = fil_data.get('atual', {}).get('fev 2026', {}).get('173', 0.0)
        expected_total_173 += val

    print(f"VALOR-ALVO (EXCEL/JSON) -> Receita Operacional Liq: R$ {expected_total_13:,.2f}")
    print(f"VALOR-ALVO (EXCEL/JSON) -> Lucro Liquido:           R$ {expected_total_173:,.2f}")

    print("Iniciando navegador invisível (Chromium) e Servidor Web local...")
    import subprocess, time
    server = subprocess.Popen([r"C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python313\python.exe", "-m", "http.server", "8000"], cwd=r"c:\dre")
    time.sleep(3)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto("http://localhost:8000/index.html")
            
            print("Aguardando o carregamento dos dados pela Engine Javascript do HTML na Porta 8000...")
            page.wait_for_selector('table.exec-table tbody tr')
            
            trs = page.query_selector_all('table.exec-table tbody tr')
            html_val_13 = 0.0
            html_val_173 = 0.0
            
            for tr in trs:
                tds = tr.query_selector_all('td')
                if len(tds) > 2:
                    desc = tds[0].inner_text()
                    total_text = tds[-2].inner_text().strip()
                    
                    try:
                        if "Receita Operacional" in desc:
                            val_str = total_text.replace('.', '').replace(',', '.')
                            if val_str: html_val_13 = float(val_str)
                        if "Lucro / Prejuizo" in desc:
                            val_str = total_text.replace('.', '').replace(',', '.')
                            if val_str: html_val_173 = float(val_str)
                    except:
                        pass

            print(f"VALOR LIDO DA TELA (HTML) -> Receita Operacional Liq: R$ {html_val_13:,.2f}")
            print(f"VALOR LIDO DA TELA (HTML) -> Lucro Liquido:           R$ {html_val_173:,.2f}")
            
            diff_13 = abs(expected_total_13 - html_val_13)
            diff_173 = abs(expected_total_173 - html_val_173)
            
            if diff_13 < 1.0 and diff_173 < 1.0:
                print("\n>>> SUCESSO ABSOLUTO! O EXCEL, A ENGINE JSON E O HTML VISUAL BATEM 100%! <<<")
            else:
                print(f"\n>>> FALHA. Diferenças encontradas: {diff_13} / {diff_173} <<<")
            
            browser.close()
    finally:
        server.terminate()

if __name__ == '__main__':
    test_visual_html()
