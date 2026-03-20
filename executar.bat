@echo off
set "PYTHON_EXE=%LOCALAPPDATA%\Programs\Python\Python313\python.exe"

if not exist "%PYTHON_EXE%" (
    echo Python nao encontrado! Tentando localizar usando 'py' ou 'python' no PATH...
    python --version >nul 2>&1
    if %errorlevel% equ 0 (
        set "PYTHON_EXE=python"
    ) else (
        py --version >nul 2>&1
        if %errorlevel% equ 0 (
            set "PYTHON_EXE=py"
        ) else (
            echo Python relamente nao encontrado. Por favor instale o Python.
            pause
            exit /b
        )
    )
)

echo Fechando qualquer servidor web anterior que tenha travado na porta 8000...
taskkill /F /IM python.exe /T >nul 2>&1

echo Gerando arquivo JSON (gerar_dre_meses.py)...
"%PYTHON_EXE%" gerar_dre_meses.py

echo Rodando auditoria (audit_centavo.py)...
"%PYTHON_EXE%" audit_centavo.py

echo Iniciando o servidor web no porto 8000 e abrindo o navegador...
start http://localhost:8000/index.html
"%PYTHON_EXE%" -m http.server 8000

pause
