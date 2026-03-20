# MEMÓRIA DO PROJETO: DRE Dashboard Comercial

**Última atualização:** 20 de Março de 2026  
**Status:** Operacional e Auditado (100% Conformidade) — Arquitetura Unificada

---

## 1. RESUMO DO PROJETO

Dashboard DRE (Demonstração do Resultado do Exercício) interativo para a rede comercial Rommanel.  
Converte dados do Excel (`Meses/*.xls`) em dashboards web premium com filtros dinâmicos e navegação integrada.

**Arquitetura Unificada:**

- Ambos os dashboards consomem agora a mesma fonte de dados: `dre_meses.json`.
- A pasta `Meses/` é o **único ponto de verdade**.
- `index.html` — DRE consolidado (todas as filiais em colunas, com filtros de Mês/Ano).
- `index_meses.html` — DRE evolução mensal (um período, com seletor de filial e histórico).

---

## 2. ARQUIVOS DO PROJETO

### 2.1 Dados Principais

| Arquivo | Função |
|---|---|
| `Meses/filiais.xls` | Cadastro de filiais (38 registros ativos) |
| `Meses/` | Pasta com 70+ arquivos XLS (Fonte Original) |
| `dre_meses.json` | JSON Unificado (Consolidado + Histórico) |
| `audit_centavo.py` | Script de auditoria de 100% de acuracidade |

### 2.2 Dashboards HTML

| Arquivo | Função |
|---|---|
| `index.html` | Dashboard Consolidado com filtros de período e deep linking para filiais. |
| `index_meses.html` | Dashboard de Evolução Mensal com seletor de filial e tratamento de parâmetros URL. |

---

## 3. COMO EXECUTAR

```powershell
# 1. Gerar o JSON unificado a partir da pasta Meses/
python gerar_dre_meses.py

# 2. (Opcional) Validar acuracidade de 1 centavo
python audit_centavo.py

# 3. Iniciar servidor local
python -m http.server 8000

# 4. Acessar os Dashboards
#    - Consolidado: http://localhost:8000/index.html
#    - Evolução:    http://localhost:8000/index_meses.html
```

---

## 4. MELHORIAS E NAVEGAÇÃO (20/03/2026)

### 4.1 Filtros Dinâmicos

O `index.html` agora permite selecionar qualquer Mês e Ano. O dashboard re-agrega os valores de todas as filiais instantaneamente via JavaScript, eliminando a dependência do antigo `gerar_dre.py` e `todas_filiais.xls`.

### 4.2 Deep Linking (Navegação Inteligente)

- **No Consolidado (`index.html`)**: Clicar no nome de uma filial no cabeçalho da tabela abre automaticamente o `index_meses.html` já filtrado para aquela filial específica.
- **Navegação de Retorno**: Ambos os dashboards possuem botões de fácil acesso para alternar entre as visões sem perder o contexto.

---

## 5. RESULTADOS DA AUDITORIA MESTRE

- **Data da Auditoria**: 20 de Março de 2026
- **Escopo**: 70 arquivos XLS vs `dre_meses.json`
- **Total de pontos verificados**: 87.675
- **Divergências**: **0 (ZERO)**
- **Conclusão**: O sistema garante 100% de acuracidade financeira em relação aos arquivos fontes da pasta `Meses/`.

---

## 6. ESTRUTURA DRE (Ordem das Contas)

- `ID 3`: 3. (=) Receita Operacional Líquida (Base de Cálculo para %)
- `ID 5`: 5. (=) Margem Bruta
- `ID 167+`: Resultado Líquido Final

As linhas com `Plano3 != 0` são detalhamentos expansíveis, enquanto `Plano3 == 0` são totalizadores de grupo.

---

## 7. HOSPEDAGEM E NUVEM (DEPLOY)

### 7.1 GitHub Pages (Publicado)

O projeto está hospedado no GitHub Pages sob a conta `athenas1200`.

- **GitHub Pages:** [https://athenas1200.github.io/dre-dashboard/](https://athenas1200.github.io/dre-dashboard/)
- **Hostgator 1:** [https://processopro.net/ro_x1z2/dre/index.html](https://processopro.net/ro_x1z2/dre/index.html)
- **Hostgator 2:** [http://consultoriasoft.com.br/dre/index.html](http://consultoriasoft.com.br/dre/index.html)


### 7.2 Atualização de Dados

Sempre que houver novos arquivos na pasta `Meses/`, siga estes passos:

1. Atualize o JSON local: `python gerar_dre_meses.py`
2. Envie para o GitHub:
   ```powershell
   git add .
   git commit -m "Atualização de dados DRE"
   git push origin main
   ```

### 7.3 Opção Hostgator

O projeto é **100% estático** (HTML/JS/JSON), o que significa que pode ser instalado em qualquer hospedagem cPanel (como Hostgator).
- **Como fazer:** Basta compactar os arquivos em um `.zip` e fazer o upload via Gerenciador de Arquivos para a pasta `public_html`.
- **Vantagem:** Permite usar um domínio próprio (ex: `financeiro.suaempresa.com.br`).

---

## 8. ATUALIZAÇÃO DIÁRIA (PASSO A PASSO)

Para atualizar o dashboard com novos dados da pasta `Meses/`, siga este processo simples:

1. **Copie os novos arquivos XLS** para a pasta `C:\dre\Meses`.
2. **Execute o arquivo `enviar_dados.bat`** (clique duplo).
   - Ele vai gerar o novo JSON e enviar para o GitHub automaticamente.
3. **No Hostgator (cPanel):**
   - Acesse **Git™ Version Control**.
   - Clique em **Manage** no repositório `dre-dashboard`.
   - Clique na aba **Pull or Deploy**.
   - Clique no botão azul **Update** para baixar os dados novos no site oficial.

---

## 9. CREDENCIAIS E ACESSOS (CONFIDENCIAL)

Abaixo estão os acessos configurados para a manutenção do ecossistema DRE:

### 9.1 GitHub
- **Usuário:** `athenas1200`
- **Senha:** `Lin281168***`
- **Personal Access Token (PAT):** `(TOKEN_OCULTADO_POR_SEGURANCA)`
- **Repositório:** `athenas1200/dre-dashboard`

### 9.2 Hostgator (cPanel)

#### Acesso 1 (ProcessoPro)
- **URL:** `https://processopro.net:2083`
- **Usuário:** `processopro`
- **Senha:** `Lin281168***`

#### Acesso 2 (ConsultoriaSoft)
- **URL:** `https://consultoriasoft.com.br:2083`
- **Usuário:** `agnaldoneves`
- **Senha:** `Lin281168***`

> [!IMPORTANT]
> Mantenha estas informações seguras. O Token do GitHub é necessário para que os scripts `.bat` funcionem sem pedir senha.



