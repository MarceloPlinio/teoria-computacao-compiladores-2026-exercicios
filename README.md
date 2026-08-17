# 📝 Exercícios — Teoria da Computação e Compiladores

**UNIFG 2026/2** · UC `0022028` · Prof. Petros Barreto
**Carga horária:** 160h — 40 aulas de 4h

Este é o repositório **público** dos exercícios. Aqui ficam as listas semanais,
a especificação do projeto MiniLang e a validação automática dos Pull Requests.

> Os **slides** das aulas ficam em repositório separado. O link é distribuído em
> sala e no ambiente virtual.

---

## 🚀 Começando (faça isso uma vez no semestre)

```bash
# 1. Faça FORK deste repositório (botão "Fork" no topo da página)

# 2. Clone o SEU fork
git clone https://github.com/SEU-USUARIO/teoria-computacao-compiladores-2026-exercicios.git
cd teoria-computacao-compiladores-2026-exercicios

# 3. Aponte para o repositório original, para receber as listas novas
git remote add upstream https://github.com/petrosbarreto/teoria-computacao-compiladores-2026-exercicios.git

# 4. Monte o ambiente Python
curl -LsSf https://astral.sh/uv/install.sh | sh
uv init && uv python pin 3.13
uv add pytest pytest-cov graphviz automata-lib ply lark

# 5. Graphviz binário (para os diagramas de autômatos)
brew install graphviz          # macOS
sudo apt install graphviz      # Debian / Ubuntu

# 6. Confira
uv run pytest --version && dot -V
```

### Antes de cada lista nova, atualize seu fork

```bash
git switch main
git pull upstream main
git push origin main
```

---

## 📤 Entregando uma lista

```bash
# 1. Branch por aula
git switch main && git pull upstream main
git switch -c aula07

# 2. Resolva dentro de exercicios/aula07/

# 3. Rode os testes ANTES de enviar
uv run pytest exercicios/aula07/ -v

# 4. Commit e push
git add exercicios/aula07
git commit -m "Aula 07: scanner com longest match"
git push -u origin aula07

# 5. Abra o Pull Request com o título EXATO:
#    [Aula 07] Seu Nome Completo
```

⚠️ **PR com título fora do padrão não é corrigido.** O formato é
`[Aula NN] Nome Completo` — colchetes, número com **dois dígitos**, e o nome
como consta na chamada.

### 🤖 Validação automática

Ao abrir o PR, o GitHub Actions roda:

| Verificação | O que acontece se falhar |
|---|---|
| `pytest` na pasta da aula | ❌ comentário no PR com a saída do erro |
| Existência de `respostas.md` | ❌ comentário pedindo o arquivo |
| Título do PR no padrão | ⚠️ aviso |
| Cobertura de testes | ℹ️ informativo |

O resultado aparece em ~1 minuto. **Você pode corrigir e dar push no mesmo
branch** — o bot roda de novo. Só corrijo manualmente PRs com o CI verde.

---

## 📂 Estrutura de cada entrega

```
exercicios/aulaNN/
├── respostas.md          # provas, deduções, tabelas, análises
├── <modulo>.py           # implementação pedida no enunciado
├── test_<modulo>.py      # seus testes (pytest)
└── img/                  # (opcional) diagramas de autômatos/árvores
```

**Regras não negociáveis:**

1. `respostas.md` em Markdown, com as seções nomeadas **como no enunciado**
   (`## Parte A`, `### A1`, ...).
2. Provas por indução **devem** conter `BASE`, `HIPÓTESE DE INDUÇÃO`, `PASSO` e
   `∎`, com `[H.I.]` marcando onde a hipótese é usada.
3. Código com **type hints** e **docstring** em cada função pública.
4. `pytest` verde no seu fork antes de abrir o PR.
5. Diagramas: ASCII dentro do `respostas.md` **ou** imagem em `img/`.

---

## 📊 Rubrica padrão de todas as listas

| Critério | Pontos | O que se avalia |
|---|---|---|
| **Corretude formal** | 40 | as respostas estão certas |
| **Justificativa / prova** | 25 | o raciocínio está completo e rigoroso |
| **Implementação e testes** | 25 | o código roda, é legível e é testado |
| **Clareza e organização** | 10 | estrutura, nomes, formatação |
| **Bônus** | +10 | o desafio final da lista |

⚠️ **Justificativa vale 25 pontos.** Resposta certa sem explicação perde um
quarto da nota. Escreva o *porquê*, sempre.

### Prazos

| | |
|---|---|
| Entrega | até a **véspera** da aula seguinte, 23h59 |
| Atraso de até 7 dias | −20 pontos |
| Atraso acima de 7 dias | não corrigido (conta como descartada) |

A nota de exercícios é a **média das 40 listas, descartando as 2 piores**.

---

## 🧮 Composição da nota final

| Instrumento | Peso |
|---|---|
| Listas semanais (40) | 40% |
| Entregas dos Blocos 2, 3 e 4 | 20% |
| Projeto MiniLang | 30% |
| Apresentação final + participação | 10% |

### 🏆 Entregas de bloco

| Entrega | Aula | O que é |
|---|---|---|
| **Bloco 2** | 12 | Pacote `automata/` — AFD, AFN, ER, Thompson, minimização, CLI |
| **Bloco 3** | 18 | Reconhecedor de LLC — autômato de pilha, GLC, FNC, CYK, Earley |
| **Bloco 4** | 24 | Simulador de Máquina de Turing + ensaio sobre computabilidade |

Cada uma exige `pytest` verde, **cobertura ≥ 90%** e `README.md` com exemplos
rodáveis.

### 🛠️ Projeto MiniLang (30%)

Um compilador completo, construído das Aulas 25 a 40.
Especificação em [`projeto/README.md`](projeto/README.md).

| Aula | Marco |
|---|---|
| 27 | Scanner (analisador léxico) |
| 32 | Parser recursivo descendente → AST |
| 35 | Analisador semântico (escopos + tipos) |
| 36 | Gerador de código de três endereços |
| 37 | Máquina virtual de pilha |
| 40 | Apresentação (15 min) + relatório |

---

## 📚 Índice das listas

| Bloco | Aulas | Tema |
|---|---|---|
| **1** | [01](exercicios/aula01) · [02](exercicios/aula02) · [03](exercicios/aula03) · [04](exercicios/aula04) · [05](exercicios/aula05) | Linguagens, gramáticas, Chomsky, técnicas de prova |
| **2** | [06](exercicios/aula06) · [07](exercicios/aula07) · [08](exercicios/aula08) · [09](exercicios/aula09) · [10](exercicios/aula10) · [11](exercicios/aula11) · [12](exercicios/aula12) | AFD, AFN, expressões regulares, minimização, bombeamento |
| **3** | [13](exercicios/aula13) · 14 · 15 · 16 · 17 · 18 | Livres de contexto, autômatos de pilha, CYK |
| **4** | 19 · 20 · 21 · 22 · 23 · 24 | Máquina de Turing, decidibilidade, P vs NP |
| **5** | 25 · 26 · 27 · 28 · 29 | Compiladores, análise léxica |
| **6** | 30 · 31 · 32 · 33 · 34 | Análise sintática |
| **7** | 35 · 36 · 37 · 38 | Semântica, código intermediário, otimização |
| **8** | 39 · 40 | Tendências e projeto final |

As listas são publicadas **na semana da aula correspondente**.

---

## 📖 Bibliografia

**Básica**
- SIPSER, M. *Introdução à Teoria da Computação*. 2ª ed. Cengage.
- AHO, A.; LAM, M.; SETHI, R.; ULLMAN, J. *Compiladores: Princípios, Técnicas e Ferramentas*. 2ª ed. Pearson.
- MENEZES, P. B. *Linguagens Formais e Autômatos*. 6ª ed. Bookman.

**Complementar**
- HOPCROFT, MOTWANI, ULLMAN. *Introduction to Automata Theory, Languages and Computation*.
- NYSTROM, R. *Crafting Interpreters* — <https://craftinginterpreters.com> (gratuito)
- COOPER, TORCZON. *Engineering a Compiler*.

---

## 🤝 Colaboração e integridade

✅ **Permitido:** discutir ideias e estratégias com colegas; consultar livros,
documentação e internet; usar assistentes de IA **desde que** você declare o uso
no `respostas.md` e **entenda** cada linha entregue.

❌ **Não permitido:** copiar código ou provas de outro aluno; entregar código que
você não é capaz de explicar em sala.

> Serei explícito: **posso pedir que você explique qualquer linha da sua
> entrega**. Não conseguir explicar zera o item — independentemente de onde o
> código veio.

---

**Dúvidas?** Abra uma [Issue](../../issues) ou pergunte em sala.
Atendimento: segundas, 30 min antes e após a aula.
