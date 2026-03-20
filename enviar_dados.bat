@echo off
set "PYTHON_EXE=python"
set "GITHUB_TOKEN=SEU_TOKEN_AQUI"
set "REPO_URL=https://athenas1200:%GITHUB_TOKEN%@github.com/athenas1200/dre-dashboard.git"

echo ==========================================
echo   ATUALIZADOR DIARIO - DRE DASHBOARD
echo ==========================================

echo 1. Gerando novo arquivo de dados (JSON)...
"%PYTHON_EXE%" gerar_dre_meses.py
if %errorlevel% neq 0 (
    echo [ERRO] Falha ao gerar o JSON. Verifique os arquivos na pasta Meses.
    pause
    exit /b
)

echo 2. Sincronizando com o GitHub...
git add .
git commit -m "Atualizacao diaria de dados - %date% %time%"
git push %REPO_URL% master:main --force

echo ==========================================
echo   SUCESSO! Dados enviados ao GitHub.
echo ==========================================
echo AGORA:
echo 1. Acesse: https://processopro.net:2083/cpsess6298582540/frontend/jupiter/git/index.html
echo 2. Clique em "MANAGE" no repositorio 'dre-dashboard'
echo 3. Clique na aba "PULL OR DEPLOY"
echo 4. Clique no botao "UPDATE" para atualizar o site oficial.
echo ==========================================
pause
