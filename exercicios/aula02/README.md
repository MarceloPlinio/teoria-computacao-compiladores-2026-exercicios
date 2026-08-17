# Exercício — Aula 02: Alfabetos, Cadeias, Operações e Linguagens

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 03 — PR `[Aula 02] Seu Nome`

---

## Parte A — Cálculos e contagem (25 pontos)

Considere `Σ = {a, b, c}` salvo indicação contrária.

**A1 (5 pts).** Calcule: (a) `|Σ⁵|`; (b) o número de cadeias de tamanho ≤ 5;
(c) o número de cadeias de tamanho exatamente 4 sobre um alfabeto de 7 símbolos.
Mostre a fórmula usada.

**A2 (5 pts).** Liste **todos** os elementos de:
(a) `{ab, c}²`  (b) `{a, ε} · {b, c}`  (c) `{ab}³`  (d) `∅²`  (e) `{ε}⁴`

**A3 (5 pts).** Para `w = abcab`, liste: todos os prefixos, todos os sufixos,
todos os prefixos **próprios**, e 5 subcadeias distintas de tamanho ≥ 2.
Quantas subcadeias distintas `w` possui no total?

**A4 (5 pts).** Prove que `|Σⁿ| = kⁿ` para `|Σ| = k`, por **indução em `n`**.

**A5 (5 pts).** Quantas cadeias de tamanho `n` sobre `{a,b}` são palíndromos?
Dê a fórmula para `n` par e `n` ímpar e justifique.

---

## Parte B — Verdadeiro ou falso, com justificativa (25 pontos)

Para cada item, responda **V** ou **F** e justifique em 1–3 linhas
(contraexemplo vale como justificativa de falsidade).

| # | Afirmação |
|---|---|
| B1 | `∅ = {ε}` |
| B2 | `∅* = {ε}` |
| B3 | `L · ∅ = L` para toda linguagem `L` |
| B4 | `(L*)* = L*` |
| B5 | `L⁺ = L*` se e somente se `ε ∈ L` |
| B6 | `(L₁L₂)ᴿ = L₂ᴿ L₁ᴿ` |
| B7 | `L₁ ∩ L₂ = ∅` implica `L₁L₂ = ∅` |
| B8 | Se `L` é finita, `L*` é finita |
| B9 | `Σ*` é enumerável |
| B10 | O conjunto de todas as linguagens sobre `Σ` é enumerável |

*(2,5 pts cada)*

---

## Parte C — Descrevendo e classificando linguagens (20 pontos)

**C1 (10 pts).** Escreva na notação `{ w ∈ Σ* | P(w) }` e dê 3 exemplos de
cadeias pertencentes + 2 não pertencentes. `Σ = {a, b}`:

1. Cadeias que começam e terminam com símbolos diferentes
2. Cadeias com número de `a`s múltiplo de 3
3. Cadeias em que nenhum `b` é seguido por outro `b`
4. Cadeias de tamanho par cujo primeiro e último símbolos são iguais
5. `{ aⁱbʲaᵏ | i + k = j }`

**C2 (10 pts).** Para cada linguagem de C1, responda: você acha que um autômato
**finito** (memória limitada, sem pilha) a reconhece? Justifique a intuição em
1 linha. *(Não precisa de prova — é um palpite fundamentado que revisitaremos
na Aula 12.)*

---

## Parte D — Implementação (30 pontos)

Crie `exercicios/aula02/linguagens.py`. Use apenas a biblioteca padrão.

Implemente, todas com **type hints**:

| Função | Descrição |
|---|---|
| `sigma_n(sigma, n)` | cadeias de tamanho exatamente `n` |
| `sigma_star(sigma, limite)` | `Σ*` truncado em `limite` |
| `concat(L1, L2)` | concatenação de linguagens |
| `potencia(L, n)` | `Lⁿ` (com `L⁰ = {ε}`) |
| `kleene(L, n_max)` | `L*` truncado |
| `positivo(L, n_max)` | `L⁺` truncado |
| `reverso(L)` | `Lᴿ` |
| `complemento(L, sigma, limite)` | `Σ* − L`, truncado |
| `prefixos(w)` / `sufixos(w)` / `subcadeias(w)` | conjuntos de cadeias |
| `ordem_canonica(sigma, n)` | primeiras `n` cadeias de `Σ*` em ordem canônica |
| `eh_palindromo(w)` | sem usar slicing reverso |

**D1 (6 pts) — Verificação empírica.** Escreva `verificar_identidades()` que
testa numericamente, para `L₁ = {"a","ab"}`, `L₂ = {"b",""}` e limite 6:

- `(L*)* == L*`
- `L·{ε} == L` e `L·∅ == ∅`
- `(L₁L₂)ᴿ == L₂ᴿ L₁ᴿ`

A função deve devolver um `dict[str, bool]`.

### Testes obrigatórios

Crie `exercicios/aula02/test_linguagens.py` com pytest, cobrindo **cada** função
(mínimo 3 asserções por função, incluindo casos com `∅` e `{ε}`):

```python
def test_kleene_do_vazio():
    assert kleene(set(), 3) == {""}          # ∅* = {ε}

def test_concat_aniquilador():
    assert concat({"a", "b"}, set()) == set()

def test_ordem_canonica():
    assert ordem_canonica({"0", "1"}, 7) == ["", "0", "1", "00", "01", "10", "11"]
```

```bash
uv run pytest exercicios/aula02/ -v
```

---

## Parte E — Desafio bônus (+10 pontos)

**E1.** Escreva `enumerar(sigma)` como um **gerador infinito** (`yield`) que
produz `Σ*` em ordem canônica indefinidamente. Use-o para imprimir a 1000ª
cadeia sobre `{a,b,c}`. Explique por que esse gerador é a prova construtiva de
que `Σ*` é enumerável — e por que **não** existe gerador análogo para o conjunto
de todas as linguagens sobre `Σ`.

---

## Entrega

```
exercicios/aula02/
├── respostas.md          # Partes A, B, C e E
├── linguagens.py         # Parte D
└── test_linguagens.py    # testes
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus E1** | +10 |
