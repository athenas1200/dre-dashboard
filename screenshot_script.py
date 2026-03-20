import subprocess, time
from playwright.sync_api import sync_playwright

print("Iniciando servidor local e navegador para capturar screenshot...")
server = subprocess.Popen([r"C:\Users\WDAGUtilityAccount\AppData\Local\Programs\Python\Python313\python.exe", "-m", "http.server", "8000"], cwd=r"c:\dre")
time.sleep(3)

try:
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})
        page.goto("http://localhost:8000/index.html", wait_until="networkidle")
        
        print("Esperando renderização dos componentes Javascript e React/Chart.js...")
        page.wait_for_selector('table.exec-table tbody tr')
        time.sleep(2) # Tempo extra para os Canvas de chart completarem as animações se existirem
        
        screenshot_path = r"C:\Users\WDAGUtilityAccount\.gemini\antigravity\brain\e23f412f-0042-4c39-bfc5-5e6fd9c1cd14\screenshot_index.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"Screenshot salvo em {screenshot_path}")
        browser.close()
finally:
    server.terminate()
