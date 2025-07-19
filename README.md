# Pull Request Analyzer 🤖📊

Um analisador inteligente de Pull Requests escrito em **Python**, que utiliza **LLMs (Large Language Models)** para gerar análises automatizadas e sugestões contextuais sobre mudanças no código.  
Neste exemplo, a LLM utilizada é a **Google Generative AI**.

---

## 🚀 Funcionalidades

- 🔍 Analisa automaticamente o conteúdo de Pull Requests
- 🧠 Utiliza uma LLM (Google GenAI) para gerar comentários inteligentes e sugestões de melhoria
- 📝 Publica os comentários diretamente no PR via GitHub API
- 🧪 A integração é feita por meio de workflows reutilizáveis no GitHub Actions

> 💡 A API Key da Google GenAI pode ser gerada gratuitamente.

---

## 🧰 Tecnologias Utilizadas

- Python 3.10+
- [Google Generative AI (gemini-pro)](https://ai.google.dev/)
- GitHub REST API (v3)
- [`requests`](https://pypi.org/project/requests/)
- [`google-generativeai`](https://pypi.org/project/google-generativeai/)

---

## 📦 Instalação

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/pull-request-analyzer.git
cd pull-request-analyzer
```

## ⚙️ Como Funciona

Este projeto é utilizado como um workflow reutilizável no GitHub Actions.

🔁 Fluxo de uso:
Um repositório externo aciona este analisador via workflow YAML, passando os parâmetros necessários (número do PR, nome do branch, etc).

O workflow do pr-analyzer é executado automaticamente, consumindo os dados do PR e utilizando a LLM para gerar a análise.

Um comentário é postado no próprio Pull Request com feedback contextualizado.

Exemplo de chamada yml no repositório que irá usar o analisador:

```
name: Call PR Analyzer

on:
  pull_request:
    types: [opened, synchronize]

jobs:
  call-analyzer:
    uses: seu-usuario/pr-analyzer/.github/workflows/analyzer.yml@main
    with:
      repository: ${{ github.repository }}
      pull_request_number: ${{ github.event.pull_request.number }}
      pr_head_ref: ${{ github.event.pull_request.head.ref }}
      pr_head_repo: ${{ github.event.pull_request.head.repo.full_name }}
    secrets:
      GENAI_API_KEY: ${{ secrets.GENAI_API_KEY }}
      PR_ANALYZER_PAT: ${{ secrets.PR_ANALYZER_PAT }}
```
