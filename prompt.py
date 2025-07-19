def generate_prompt(repo_name: str, diff_content: str, pr_title: str, pr_number: int) -> str:
    """Monta o prompt para o modelo com o diff e informações do PR."""
    prompt_template = f"""
        Você é um especialista em analisar pull requests de projetos de software. Sua tarefa é revisar o diff fornecido abaixo e fornecer uma análise detalhada, identificando potenciais problemas e sugestões de melhoria.

        {prompt_definer(repo_name)}

        Formato da sua resposta:

        **Análise do Pull Request:**

        **Potenciais Problemas e Sugestões de Melhoria:**
        - [Lista de problemas identificados e sugestões específicas]

        **Comentários Adicionais:**
        - [Outros comentários relevantes]

        **Diff do Pull Request:**
    """
    info = f"\n\nnome do pr: {pr_title} numero {pr_number}"
    return prompt_template + diff_content + info

def prompt_definer(repo: str) -> str:
    prompts = {
        'exemplo_nome_repositorio_api': api_prompt,
        'exemplo_nome_repositorio_app': app_prompt,
    }

    try:
        return prompts[repo]()
    except KeyError:
        raise ValueError(f"No prompt defined for repository: '{repo}'")

def app_prompt():
    return """
        Considere os seguintes critérios ao revisar código em React (JavaScript):

        ✦ Qualidade e Clareza do Código
        - O código é legível, com nomes descritivos e organização lógica?
        - Evitar estruturas condicionais com `else` (usar early return).
        - Evitar código redundante ou duplicado.
        - Proibir qualquer tipo de código comentado no repositório.

        ✦ Estilo e Boas Práticas
        - Proibir uso de `console.log`, `debugger` ou prints similares em produção.
        - Proibir uso de estilos inline (`style={{ ... }}`); utilizar classes ou styled-components.
        - Adotar consistência no uso de hooks e evitar lógica complexa nos componentes.

        ✦ Estado e Mutabilidade
        - Alertar se uma variável do `initialState` for diretamente modificada (imutabilidade deve ser respeitada).
        - Preferir `useReducer` quando o estado for complexo.
        - Não modificar estado diretamente (`state = ...`), sempre usar `setState` ou função do hook apropriado.

        ✦ Arquitetura e Estrutura do Projeto
        - Adesão à convenção e estrutura de pastas do projeto.
        - Componentes devem ser pequenos e de responsabilidade única.
        - Separar lógica de negócios em hooks personalizados ou serviços externos quando necessário.

        ✦ Segurança e Performance
        - Verificar por vazamentos de memória (event listeners não limpos, efeitos sem deps, etc.).
        - Evitar re-renderizações desnecessárias (uso incorreto de deps em `useEffect`, funções inline em JSX, etc.).
        - Evitar manipulação direta do DOM (preferir refs).

        ✦ Pull Requests e Convenções
        - O nome do PR deve seguir o padrão: `feature/TRM-<número>-<descricao>` ou `hotfix/TRM-<número>-<descricao>`.
        - Validar se a descrição do PR explica claramente a motivação e as mudanças.
    """


def api_prompt():
    return """
        Considere os seguintes critérios ao revisar código PHP com Laravel:

        ✦ Qualidade e Clareza
        - O código está limpo, legível e conciso?
        - Evitar redundância e complexidade desnecessária.
        - Não utilizar estruturas `else` (usar early return).
        - Proibir qualquer código comentado no repositório.

        ✦ Boas Práticas e Convenções
        - Seguir as convenções do projeto (nomenclatura, estrutura, organização).
        - Nome do Pull Request deve seguir o padrão: `feature/TRM-<número>-<descricao>` ou `hotfix/TRM-<número>-<descricao>`.
        - Métodos em services devem ter responsabilidade única, preferencialmente via `__invoke()`.

        ✦ Segurança e Estabilidade
        - Proibir uso de `dd()`, `dump()`, `var_dump()` ou similares.
        - Proibir o uso direto de `env()`, utilizar `config()` como intermediário.
        - Não permitir rotas sem middleware de permissionamento/autorização.
        - Proibir `try-catch`; utilizar tratamento de erro centralizado, se aplicável.

        ✦ Arquitetura e Organização
        - Controllers devem sempre retornar uma `Response`.
        - Queries devem ser encapsuladas via `scope` nos models.
        - Migrations devem ter nomes terminando em `_table`.
        - Proibir migrations com campos `id` e `timestamps` no array `fillable`.

        ✦ PHP Moderno e Laravel Atual
        - Permitir apenas promotion de propriedades no construtor (`constructor property promotion`).
    """