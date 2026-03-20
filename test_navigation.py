import subprocess, time
from playwright.sync_api import sync_playwright

print("Iniciando servidor local e Chrome (Playwright)...")
server = subprocess.Popen([r"C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python313\python.exe", "-m", "http.server", "8000"], cwd=r"c:\dre")
time.sleep(3)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        
        print("Passo 1: Acessando index.html...")
        page.goto("http://localhost:8000/index.html", wait_until="networkidle")
        page.wait_for_selector('table.exec-table tbody tr')
        time.sleep(2)
        
        print("Testando navegação: Buscando botão 'Evolução Mensal'...")
        # Procura o botão que contém "Evolução Mensal"
        page.locator("button:has-text('Evolução Mensal')").click()
        
        print("Passo 2: Aguardando redirecionamento...")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        print("URL atual do navegador:", page.url)
        
        if "index_meses.html" in page.url:
            print("SUCESSO: A navegação funcionou perfeitamente!")
        else:
            print("FALHA: A navegação não foi para o arquivo correto.")
        
        screenshot_path = r"C:\Users\WDAGUtilityAccount\.gemini\antigravity\brain\e23f412f-0042-4c39-bfc5-5e6fd9c1cd14\screenshot_navegacao.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot do destino salvo em {screenshot_path}")

        # Testa o caminho reverso (voltar)
        if page.locator("button:has-text('Consolidado')").count() > 0:
            print("Testando navegação reversa (voltar para o Consolidado)...")
            page.locator("button:has-text('Consolidado')").click()
            page.wait_for_load_state("networkidle")
            if "index.html" in page.url:
                print("SUCESSO: O caminho de volta também funciona!")
            else:
                print("ERRO: O caminho de volta não funcionou.")

        browser.close()
finally:
    server.terminate()
