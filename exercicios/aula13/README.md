# Exercício — Aula 13: Gramáticas Livres de Contexto e Ambiguidade

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 14 — PR `[Aula 13] Seu Nome`

---

## Parte A — Projetando GLCs (30 pontos)

Para cada linguagem: (i) dê `G = (V, Σ, P, S)` **completa**, (ii) derive uma
cadeia de tamanho ≥ 5 mostrando os passos, (iii) desenhe a árvore de derivação,
(iv) **verifique com o gerador BFS** (Parte E) antes de entregar.

| # | Linguagem | Pts |
|---|---|---|
| A1 | `{ aⁿb²ⁿ \| n ≥ 0 }` | 3 |
| A2 | `{ aⁱbʲ \| i ≥ j ≥ 0 }` | 3 |
| A3 | `{ w ∈ {a,b}* \| #ₐ(w) = #_b(w) }` | 4 |
| A4 | `{ w ∈ {a,b}* \| #ₐ(w) = 2·#_b(w) }` | 4 |
| A5 | `{ aⁱbʲcᵏ \| i = j + k }` | 4 |
| A6 | `{ wcwᴿ \| w ∈ {a,b}* }` | 3 |
| A7 | parênteses `()`, `[]`, `{}` corretamente aninhados | 3 |
| A8 | `{ aⁿbᵐ \| n ≠ m }` | 3 |
| A9 | comentários `/* ... */` **aninhados** | 3 |

**A9 — pergunta obrigatória:** por que comentários aninhados **não** podem ser
reconhecidos por uma expressão regular? Cite o resultado da Aula 12 que sustenta
sua resposta. E por que C **não** permite aninhamento, enquanto OCaml e Rust
permitem?

---

## Parte B — Árvore de derivação x AST (10 pontos)

Considere a gramática estratificada:

```
E → E + T | T
T → T * F | F
F → ( E ) | num
```

**B1 (5 pts).** Para `2 * ( 3 + 4 )`: desenhe a **árvore de derivação completa**
(todos os nós `E`, `T`, `F`) e, ao lado, a **AST**. Conte os nós de cada uma.

**B2 (5 pts).** Responda:
(a) Onde foram os parênteses na AST?
(b) O que acontece com as cadeias `E → T → F` na tradução para AST?
(c) Por que as fases seguintes do compilador usam a AST e não a árvore de
derivação? Dê **duas** razões concretas.

---

## Parte C — Ambiguidade (30 pontos)

**C1 (10 pts).** Exiba **duas árvores distintas** para cada par:

| # | Gramática | Cadeia |
|---|---|---|
| a | `S → SS \| a` | `aaa` |
| b | `E → E+E \| E*E \| id` | `id+id*id` |
| c | `S → aS \| Sa \| a` | `aa` |
| d | `C → if C \| if C else C \| x` | `if if x else x` |

**C2 (12 pts).** Reescreva **sem ambiguidade**:

```
E → E + E | E - E | E * E | E / E | E % E | E ^ E | - E | ! E | ( E ) | num
```

Precedência (menor → maior): `+ -` < `* / %` < `- ! unários` < `^`.
Associatividade: binários aritméticos à **esquerda**; `^` à **direita**;
unários à direita.

Justifique **cada nível criado** e verifique com `conta_arvores` que
`1-2-3`, `2^3^2`, `-2^2` e `1+2*3^2` têm **exatamente uma** árvore cada.
Diga como cada uma agrupou.

**C3 (4 pts).** A gramática `S → aSb | ab | ε` é ambígua? Prove ou justifique
rigorosamente. *(Há uma pegadinha — pense em qual cadeia testar.)*

**C4 (4 pts).** Explique por que `S → SS | a | ε` gera **infinitas** árvores para
a cadeia `a`. Enuncie a condição estrutural geral que causa isso e dê outro
exemplo de gramática que a satisfaz.

---

## Parte D — Dangling else (10 pontos)

**D1 (4 pts).** Para `C → if E then C | if E then C else C | outro`, desenhe as
duas árvores de `if E then if E then outro else outro` e diga qual é a
interpretação adotada pelas linguagens reais.

**D2 (4 pts).** Escreva a gramática **casada/não casada** que remove a
ambiguidade. Explique **exatamente** qual restrição impede o `if` interno de
capturar o `else`.

**D3 (2 pts).** Pesquise o bug **"goto fail"** do iOS/macOS (fevereiro de 2014).
Relacione-o ao *dangling else* e às regras de estilo que exigem chaves
obrigatórias. Em 5 linhas: o formalismo teria evitado o bug?

---

## Parte E — Implementação (20 pontos)

Crie `exercicios/aula13/glc.py`. Represente a gramática como
`dict[str, list[list[str]]]` (variável → lista de corpos; corpo `[]` = `ε`).

| Função | Descrição | Pts |
|---|---|---|
| `gerar(G, inicial, n, tam_max)` | as `n` menores sentenças de `L(G)`, por BFS/heap | 4 |
| `conta_arvores(G, inicial, palavra)` | nº de árvores de derivação (com memoização) | 5 |
| `derivacao_esquerda(G, inicial, palavra)` | formas sentenciais da derivação leftmost, ou `None` | 4 |
| `arvore(G, inicial, palavra)` | **uma** árvore como dict aninhado | 3 |
| `para_ascii(arv)` | renderiza a árvore com `├──` / `└──` | 2 |
| `buscar_ambiguidade(G, inicial, tam_max)` | `(sentença, nº árvores)` ou `None` | 2 |

### Testes obrigatórios

`exercicios/aula13/test_glc.py`:

```python
G_EXPR = {"E": [["E","+","T"],["T"]],
          "T": [["T","*","F"],["F"]],
          "F": [["(","E",")"],["id"]]}
G_AMB  = {"E": [["E","+","E"],["E","*","E"],["id"]]}
G_ANBN = {"S": [["a","S","b"],[]]}

def test_gerar_anbn():
    assert gerar(G_ANBN, "S", 4, 10) == ["", "a b", "a a b b", "a a a b b b"]

def test_nao_ambigua():
    assert conta_arvores(G_EXPR, "E", ["id","+","id","*","id"]) == 1

def test_ambigua():
    assert conta_arvores(G_AMB, "E", ["id","+","id","*","id"]) == 2
    assert conta_arvores(G_AMB, "E", ["id","+","id","+","id"]) == 2

def test_associatividade_esquerda():
    # 1-2-3 deve agrupar como (1-2)-3
    arv = arvore(G_SUB, "E", ["1","-","2","-","3"])
    # o filho ESQUERDO da raiz deve ser o subtrator composto
    assert arv["filhos"][0]["sim"] == "E"
    assert len(arv["filhos"][0]["filhos"]) == 3

def test_associatividade_direita_potencia():
    # 2^3^2 deve agrupar como 2^(3^2)
    arv = arvore(G_POT, "F", ["2","^","3","^","2"])
    assert arv["filhos"][2]["sim"] == "F"      # recursão à DIREITA

def test_estratificada_nao_ambigua():
    for w in ["1 - 2 - 3", "2 ^ 3 ^ 2", "- 2 ^ 2", "1 + 2 * 3 ^ 2"]:
        assert conta_arvores(G_C2, "E", w.split()) == 1, w

def test_buscar_ambiguidade():
    assert buscar_ambiguidade(G_AMB, "E", 7) is not None
    assert buscar_ambiguidade(G_EXPR, "E", 9) is None

def test_derivacao_esquerda_rejeita():
    assert derivacao_esquerda(G_ANBN, "S", ["a","b","a"]) is None
```

```bash
uv run pytest exercicios/aula13/ -v
```

---

## Parte F — Reflexão obrigatória (sem pontos, mas zera a Parte E se ausente)

Seu `buscar_ambiguidade` devolveu `None` para a gramática estratificada de C2.

**Isso prova que ela não é ambígua?** Responda em `respostas.md`, em ~10 linhas,
referenciando:
- a **indecidibilidade** do problema da ambiguidade de GLCs;
- a diferença entre **semi-decisor** e **decisor**;
- por que `bison` reporta *conflitos* em vez de *ambiguidade*.

---

## Parte G — Desafio bônus (+10 pontos)

**G1.** Escreva a GLC de um **subconjunto real de JSON**:

```json
{"nome": "Ana", "idade": 30, "tags": ["a", "b"], "ativo": true, "meta": null}
```

Suporte: objetos, arrays, strings (com escapes), números (inteiro, real,
expoente), `true`, `false`, `null`, aninhamento arbitrário.

Depois:
(a) Prove que sua gramática é **não ambígua** para 20 documentos de teste usando
`conta_arvores`.
(b) Escreva `json_para_python(arvore)` que percorre a árvore de derivação e
constrói o objeto Python correspondente. Compare com `json.loads` em 20 casos.
(c) Explique por que JSON **não** pode ser validado por expressão regular, e o
que exatamente na sua gramática exige a pilha.

---

## Entrega

```
exercicios/aula13/
├── respostas.md        # Partes A–D, F e G (árvores em ASCII ou imagem)
├── glc.py              # Parte E
├── json_glc.py         # Parte G (bônus)
└── test_glc.py         # testes
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus G1** | +10 |
