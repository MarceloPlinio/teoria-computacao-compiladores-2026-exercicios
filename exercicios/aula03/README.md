# Exercício — Aula 03: Gramáticas Formais, Derivações e Árvores

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 04 — PR `[Aula 03] Seu Nome`

---

## Parte A — Lendo gramáticas (20 pontos)

Para cada gramática, (i) descreva `L(G)` na notação `{ ... | ... }`,
(ii) liste as 4 menores cadeias geradas, (iii) dê uma cadeia sobre o alfabeto
que **não** pertence a `L(G)`.

| # | Produções |
|---|---|
| A1 | `S → 0S1 \| 01` |
| A2 | `S → aSa \| bSb \| a \| b` |
| A3 | `S → AB`, `A → aAb \| ε`, `B → cB \| ε` |
| A4 | `S → aS \| Sb \| ε` |
| A5 | `S → 1A`, `A → 0A \| 1A \| ε` (sobre `{0,1}`) |

*(4 pts cada)*

---

## Parte B — Escrevendo gramáticas (25 pontos)

Escreva `G = (V, Σ, P, S)` **completa** (os 4 componentes explícitos) para cada
linguagem. Depois **derive uma cadeia** de tamanho ≥ 4 e **desenhe a árvore**.

| # | Linguagem |
|---|---|
| B1 | `{ w ∈ {a,b}* \| w tem número par de b's }` |
| B2 | `{ aⁱbʲ \| j = 2i, i ≥ 0 }` |
| B3 | `{ aⁱbʲcᵏ \| i + k = j }` |
| B4 | `{ w ∈ {a,b}* \| w ≠ wᴿ }` (não palíndromos) |
| B5 | Identificadores válidos: letra seguida de letras, dígitos ou `_` |

*(5 pts cada)*

---

## Parte C — Derivações e árvores (20 pontos)

Considere:

```
E → E + T | T
T → T * F | F
F → ( E ) | id
```

**C1 (5 pts).** Dê a derivação **mais à esquerda** completa de `id * ( id + id )`.

**C2 (5 pts).** Dê a derivação **mais à direita** da mesma cadeia.

**C3 (5 pts).** Desenhe a árvore de derivação. Ela é a mesma para C1 e C2?
Explique por quê.

**C4 (5 pts).** Quantos passos tem cada derivação? Formule e justifique a
relação entre o número de passos de uma derivação e o número de nós internos
da árvore.

---

## Parte D — Ambiguidade (20 pontos)

**D1 (6 pts).** Prove que `S → SS | a | ε` é ambígua, exibindo **duas árvores
distintas** para a cadeia `aa`.

**D2 (7 pts).** Reescreva de forma **não ambígua**:

```
E → E + E | E - E | E * E | E / E | E ^ E | - E | ( E ) | num
```

Requisitos de precedência (do menor para o maior): `+ -` < `* /` < menos unário
< `^`. Associatividade: `+ - * /` à esquerda; `^` à **direita**; menos unário à
direita. Justifique cada nível criado.

**D3 (7 pts).** Considere:

```
C → if E then C | if E then C else C | cmd
```

(a) Exiba as duas árvores para `if E then if E then cmd else cmd`.
(b) Explique a solução "comando casado / não casado".
(c) Por que a maioria das linguagens reais mantém a gramática ambígua e resolve
no parser? Cite uma consequência prática dessa escolha para o programador.

---

## Parte E — Implementação (15 pontos)

Crie `exercicios/aula03/gramatica.py`. Represente a gramática como
`dict[str, list[str]]` (variável → lista de lados direitos; `""` = `ε`).

| Função | Descrição |
|---|---|
| `derivar_esquerda(G, alvo, limite)` | devolve a lista de formas sentenciais da derivação mais à esquerda de `alvo`, ou `None` |
| `gerar(G, n, tam_max)` | as `n` menores cadeias de `L(G)`, por BFS |
| `conta_arvores(G, alvo, limite)` | número de árvores de derivação distintas de `alvo` |
| `eh_ambigua(G, tam_max)` | `True` se existir cadeia com ≥ 2 árvores; devolva também a cadeia testemunha |

### Testes obrigatórios

`exercicios/aula03/test_gramatica.py`:

```python
G_ANBN = {"S": ["aSb", ""]}
G_AMB  = {"S": ["SS", "a", ""]}
G_EXPR = {"E": ["E+T", "T"], "T": ["T*F", "F"], "F": ["(E)", "id"]}

def test_gerar():
    assert gerar(G_ANBN, 4, 10) == ["", "ab", "aabb", "aaabbb"]

def test_ambiguidade():
    ambigua, testemunha = eh_ambigua(G_AMB, 4)
    assert ambigua
    assert conta_arvores(G_AMB, "aa", 8) >= 2

def test_nao_ambigua():
    assert conta_arvores(G_EXPR, "id+id*id", 12) == 1
```

```bash
uv run pytest exercicios/aula03/ -v
```

---

## Parte F — Desafio bônus (+10 pontos)

**F1.** Para `S → SS | a`, calcule `conta_arvores` para `aⁿ` com `n = 1..7`.
Compare com a sequência de **números de Catalan** `Cₙ = (2n)! / ((n+1)! n!)`.
Explique a correspondência: por que contar árvores binárias de derivação dá
Catalan? Escreva a demonstração combinatória em ~10 linhas.

---

## Entrega

```
exercicios/aula03/
├── respostas.md          # Partes A–D e F (árvores em ASCII ou imagem)
├── gramatica.py          # Parte E
└── test_gramatica.py     # testes
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus F1** | +10 |
