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
- **Consolidado (`index.html`)**: Agora permite selecionar "Todos os Meses" e/ou "Todos os Anos" (2025+2026), renderizando automaticamente uma soma consolidada flexível com o layout `DRE Consolidado Estilizado`. Por padrão, ele sempre é aberto na seleção "Mês: Todos, Ano: Todos, Filial: Consolidadas".
- **Evolução Mensal (`index_meses.html`)**: Inicia apontando sempre para a Filial Consolidada, no Ano atual e Mês corrente.

### 4.2 Exportação Nativa Estilizada
Os relatórios agora exportam o `.xlsx` completo (usando `xlsx-js-style` via CDN). Estilização inclui cabeçalhos azuis/teals, negritos para níveis agrupadores, percentuais calculados e números negativos renderizados em font vermelha nativa no Excel.

### 4.3 Metas no Gráfico de Pareto (Análise DRE)
No dashboard executivo `analise_dre.html`, o gráfico Pareto 80/20 agora apresenta duas "linhas de corte" traçadas:
- **Meta Venda** (Tracejado Laranja/Amarelo)
- **Meta Lucro** (Tracejado Verde Escuro)
*Observação técnica:* Como não existe uma tabela de metas nativa no arquivo `MESES/`, as variáveis `META_VENDA = 300000` e `META_LUCRO = 50000` estão declaradas no Javascript localmente. Apenas abra `analise_dre.html` em um editor e modifique os valores numéricos onde consta "Definição das Metas".

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

- **Hostgator 1:** [https://processopro.net/dre/index.html](https://processopro.net/dre/index.html)
- **Hostgator 2:** [https://consultoriasoft.com.br/dre/index.html](https://consultoriasoft.com.br/dre/index.html)


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

### 8.1 Opção de Envio Rápido via Script `.bat`
Para atualizar o JSON gerado localmente pelas planilhas para o GitHub:
1. Copie os arquivos `.xls` recém baixados do sistema para a pasta `C:\dre\Meses`.
2. Clique duplo em `enviar_dados.bat`. Ele gera um novo banco e empurra para a Origin. *(Requer substituição de Token no código caso você clonar o repo num notebook novo)*.
3. No cPanel de cada Hostgator, acesse o botão "Update from Remote" na aba "Git™ Version Control".

### 8.2 Opção Direta via FTP (Recomendado para Emergências)
O deploy final da versão estabilizada via FTP diretamente do computador local dispensa o Git.
- Use FileZilla ou PowerShell.
- **Host**: `consultoriasoft.com.br`
- **Porta**: 21
- **Diretório Remoto**: `/public_html/dre/`
- Transfira apenas os arquivos `*.html` e `dre_meses.json`.

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



