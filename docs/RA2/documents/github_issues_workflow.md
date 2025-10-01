# Como Usar GitHub Issues no Projeto

## Conceitos Básicos
- **Issue** → Uma tarefa, bug ou item de trabalho a ser feito.  
- **Milestone** → Um agrupador de issues (ex: "Foundation & Setup").  
- **Labels** → Etiquetas para classificar issues (ex: `documentation`, `testing`).  
- **Assignee** → Pessoa responsável pela issue.  
- **Pull Request (PR)** → Quando alguém implementa a solução no código e abre para revisão.

> Dica: se você escrever na descrição de um PR `fixes #7`, o GitHub fecha a issue #7 automaticamente quando o PR for mergeado.

---

## Workflow Sugerido

1. **Planejamento**
   - Criar uma issue para cada tarefa.  
   - Atribuir milestone (ex: *Foundation & Setup*).  
   - Definir labels (ex: `parser`, `setup`, `testing`).  
   - Atribuir responsável (assignee).  

2. **Execução**
   - O responsável cria uma branch (ex: `feature/lerTokens`).  
   - Implementa a solução.  
   - Abre um Pull Request com `fixes #X` na descrição.  

3. **Revisão**
   - Outro colega revisa o PR.  
   - Se aprovado → merge no `main`.  
   - A issue associada fecha automaticamente.  

4. **Acompanhamento**
   - Ver progresso das milestones no GitHub (quantas issues abertas/fechadas).  
   - Discutir issues em reunião rápida, se necessário.  

---

## Exemplo de Workflow

- Criar issue **#5: Implementar `construirGramatica`**  
  - Milestone: *Core Development*  
  - Labels: `grammar`, `function-implementation`  
  - Assignee: Student 1  

- Student 1 cria branch `feature/construirGramatica`.  
- Faz a implementação e abre um PR com descrição:  
  ```
  Implementação inicial da função construirGramatica.
  fixes #5
  ```  
- Quando o PR é mergeado → a issue #3 fecha automaticamente.  
- O milestone mostra que o projeto avançou.  

---

## Resumindo
- Issues organizam o trabalho.  
- Labels e milestones ajudam na visão geral.  
- PRs com `fixes #X` conectam código a issues.  
- O GitHub atualiza automaticamente o progresso.  
