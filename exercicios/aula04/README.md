# Exercício — Aula 04: Hierarquia de Chomsky

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 05 — PR `[Aula 04] Seu Nome`

---

## Parte A — Classificando gramáticas (25 pontos)

Para cada gramática, indique o tipo Chomsky **mais restrito** (3, 2, 1 ou 0) e
**cite a produção** que impede o tipo imediatamente superior.

| # | Produções |
|---|---|
| A1 | `S → 0S \| 1S \| ε` |
| A2 | `S → S0 \| S1 \| 0 \| 1` |
| A3 | `S → 0S1 \| ε` |
| A4 | `S → 0S \| S1 \| ε` |
| A5 | `S → aSBc \| abc`, `cB → Bc`, `bB → bb` |
| A6 | `S → AB`, `A → aA \| ε`, `B → bB \| ε` |
| A7 | `AB → BA`, `S → AB`, `A → a`, `B → b` |
| A8 | `S → aA`, `aA → ε` |
| A9 | `S → aB \| ε`, `B → bS` |
| A10 | `S → ε`, `S → aSa`, `S → b` |

*(2,5 pts cada)*

---

## Parte B — Localizando linguagens (25 pontos)

Para cada linguagem, indique a classe **mais restrita** (Regular / LLC / LSC /
Recursiva / RE / não RE) e justifique em 1–3 linhas. Onde couber, dê a gramática
ou o autômato que sustenta sua resposta.

| # | Linguagem |
|---|---|
| B1 | `{ w ∈ {0,1}* \| w termina em 00 }` |
| B2 | `{ 0ⁿ1ⁿ \| n ≥ 0 }` |
| B3 | `{ 0ⁿ1ⁿ2ⁿ \| n ≥ 0 }` |
| B4 | `{ ww \| w ∈ {a,b}* }` |
| B5 | `{ wwᴿ \| w ∈ {a,b}* }` |
| B6 | `{ aⁿ \| n é um quadrado perfeito }` |
| B7 | `{ aⁿ \| n é primo }` |
| B8 | `{ ⟨M⟩ \| M é uma MT que aceita ao menos uma cadeia }` |
| B9 | `{ ⟨M⟩ \| M é uma MT que NÃO aceita nenhuma cadeia }` |
| B10 | JSON sintaticamente válido |

*(2,5 pts cada)*

Atenção especial: **B4 e B5 não estão na mesma classe.** Explique a diferença.

---

## Parte C — Gramática ≠ Linguagem (15 pontos)

**C1 (5 pts).** Dê uma gramática de **tipo 2** que gere uma linguagem
**regular**. Depois dê uma gramática de **tipo 3** para a mesma linguagem,
provando que a linguagem é regular apesar da primeira gramática.

**C2 (5 pts).** Dê uma gramática de **tipo 1** que gere uma linguagem **livre de
contexto**, e a GLC equivalente.

**C3 (5 pts).** Explique, com precisão, por que a afirmação abaixo é **falsa**:

> "Se uma gramática é de tipo 2 e não de tipo 3, então a linguagem gerada não é
> regular."

---

## Parte D — Compiladores e a hierarquia (15 pontos)

**D1 (5 pts).** Classifique cada regra da linguagem C na hierarquia e indique a
**fase do compilador** responsável por verificá-la:

| Regra |
|---|
| a) identificadores começam com letra ou `_` |
| b) todo `{` tem um `}` correspondente |
| c) toda variável usada foi declarada |
| d) o número de argumentos de uma chamada casa com a assinatura |
| e) literais de string são delimitados por `"` |
| f) `return` em função `void` não pode ter expressão |

**D2 (5 pts).** A linguagem `{ wcw | w ∈ {a,b}* }` não é livre de contexto.
Explique, em termos práticos, qual regra de linguagens de programação esse fato
formal impede o parser de verificar — e como os compiladores reais resolvem.

**D3 (5 pts).** Python usa **indentação** para delimitar blocos. Pesquise: como
o *tokenizer* do CPython lida com isso (tokens `INDENT`/`DEDENT`)? Por que essa
solução é necessária, e o que ela nos diz sobre a expressividade das gramáticas
livres de contexto?

---

## Parte E — Implementação (20 pontos)

Crie `exercicios/aula04/chomsky.py`.

**E1 (8 pts).** `classificar(V, Sigma, P, S) -> int` — devolve 3, 2, 1 ou 0.
Represente produções como **listas de símbolos**, para suportar terminais
multi-caractere:

```python
Producao = tuple[list[str], list[str]]
P = [(["S"], ["if", "E", "then", "S"]), (["S"], ["cmd"])]
```

**E2 (7 pts).** `explicar(V, Sigma, P, S) -> str` — devolve o tipo **e** a
produção que bloqueou o tipo superior, em português:

```python
>>> explicar({"S"}, {"a", "b"}, [(["S"], ["a","S","b"]), (["S"], [])], "S")
'Tipo 2. Não é tipo 3: a produção S → aSb tem terminal após a variável.'
```

**E3 (5 pts).** `valida_gramatica(V, Sigma, P, S) -> list[str]` — devolve a
lista de problemas estruturais encontrados:

- `V ∩ Σ ≠ ∅`
- `S ∉ V`
- símbolo no lado direito que não está em `V ∪ Σ`
- lado esquerdo sem nenhuma variável
- variável **inalcançável** a partir de `S`
- variável **improdutiva** (não deriva nenhuma cadeia de terminais)

### Testes obrigatórios

`exercicios/aula04/test_chomsky.py` — **no mínimo 2 gramáticas por tipo**:

```python
def test_tipo3_direita():
    assert classificar({"S"}, {"a","b"},
        [(["S"], ["a","S"]), (["S"], ["b"])], "S") == 3

def test_nao_mistura_orientacao():
    # A → aB e A → Ba juntas NÃO são tipo 3
    assert classificar({"S","A"}, {"a","b"},
        [(["S"], ["a","A"]), (["A"], ["S","b"]), (["A"], [])], "S") == 2

def test_tipo1_anbncn():
    assert classificar({"S","B"}, {"a","b","c"},
        [(["S"], ["a","B","S","c"]), (["S"], ["a","B","c"]),
         (["B","a"], ["a","B"]), (["B","b"], ["b","b"])], "S") == 1

def test_tipo0_encurta():
    assert classificar({"S","A","B"}, {"a","b"},
        [(["S"], ["a","A","B","b"]), (["A","B"], [])], "S") == 0

def test_valida_detecta_improdutiva():
    problemas = valida_gramatica({"S","X"}, {"a"},
        [(["S"], ["a"]), (["X"], ["X","a"])], "S")
    assert any("improdutiva" in p.lower() for p in problemas)
```

```bash
uv run pytest exercicios/aula04/ -v
```

---

## Parte F — Desafio bônus (+10 pontos)

**F1.** Construa uma gramática **sensível ao contexto** para
`L = { ww | w ∈ {a,b}* }` e demonstre a derivação de `abab` passo a passo.
Depois explique, sem prova formal, por que nenhuma GLC gera essa linguagem —
enquanto `{ wwᴿ }` é livre de contexto. Qual a diferença estrutural
(o que a pilha consegue e o que não consegue fazer)?

---

## Entrega

```
exercicios/aula04/
├── respostas.md        # Partes A–D e F
├── chomsky.py          # Parte E
└── test_chomsky.py     # testes
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus F1** | +10 |
