# Exercício — Aula 09: Conversão AFN → AFD e Minimização

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 10 — PR `[Aula 09] Seu Nome`

> ⚠️ **Este código é parte da Entrega do Bloco 2** (simulador de autômatos,
> cobrado na Aula 12). Trate-o como código de produção: type hints, docstrings,
> testes.

---

## Parte A — Construção de subconjuntos à mão (25 pontos)

### A1 (12 pts) — AFN-ε

| `δ` | `a` | `b` | `ε` |
|---|---|---|---|
| **→ 1** | {1, 2} | {1} | {3} |
| **2** | ∅ | {4} | ∅ |
| **3** | {3} | ∅ | {5} |
| ***4** | {4} | {4} | ∅ |
| **5** | ∅ | {4} | ∅ |

(a) Calcule `E({1})`, `E({2})`, `E({3})`, `E({1,4})`.
(b) Execute a construção **completa**, mostrando cada conjunto novo na ordem de
descoberta e nomeando `A, B, C, ...`.
(c) Dê a tabela `Δ` do AFD, marcando inicial e finais.
(d) Quantos estados? Compare com `2^5 = 32` e explique a diferença.
(e) Apareceu o estado `∅`? Ele é necessário? Justifique.

### A2 (13 pts) — Sem `ε`

| `δ` | `0` | `1` |
|---|---|---|
| **→ p** | {p, q} | {p} |
| **q** | {r} | {r} |
| **r** | ∅ | {s} |
| ***s** | {s} | {s} |

(a) Converta para AFD (só alcançáveis).
(b) Descreva `L` em português.
(c) Minimize o AFD resultante (Parte B tem o algoritmo) e diga quantos estados sobraram.

---

## Parte B — Minimização à mão (25 pontos)

AFD `M`:

| `δ` | `0` | `1` |
|---|---|---|
| **→ q0** | q1 | q2 |
| **q1** | q3 | q4 |
| ***q2** | q4 | q3 |
| ***q3** | q5 | q5 |
| ***q4** | q5 | q5 |
| **q5** | q5 | q5 |
| **q6** | q0 | q6 |

**B1 (5 pts).** Quais estados são **inalcançáveis** de `q0`? Quais são
**inúteis** (não alcançam `F`)? Remova os inalcançáveis.

**B2 (12 pts).** Preenchimento de tabela: desenhe a tabela triangular, marque os
pares com exatamente um final e propague, **mostrando cada iteração**. Para cada
par marcado, registre o **sufixo distintivo**.

**B3 (5 pts).** Liste as classes de equivalência e dê a tabela do AFD mínimo.

**B4 (3 pts).** Descreva `L(M)`. Quantas classes tem `≡_L`? Confere com o número
de estados do AFD mínimo?

---

## Parte C — Myhill-Nerode (15 pontos)

**C1 (5 pts).** Use Myhill-Nerode para provar que
`L = { 0ⁿ1ⁿ | n ≥ 0 }` **não** é regular. Exiba a família infinita de cadeias
duas a duas distinguíveis e o sufixo distintivo de cada par.

**C2 (5 pts).** Idem para `L = { w ∈ {a,b}* | #ₐ(w) = #_b(w) }`.

**C3 (5 pts).** Para `L = { w ∈ {0,1}* | w termina em 01 }`, **liste** as classes
de equivalência de `≡_L` (dê um representante e a caracterização de cada uma) e
conclua quantos estados o AFD mínimo tem. Confirme construindo o AFD.

---

## Parte D — Implementação (35 pontos)

Crie `exercicios/aula09/conversao.py`, importando `AFD` (Aula 06) e `AFN` (Aula 08).

**D1 (8 pts).** `afn_para_afd(N) -> AFD` — construção de subconjuntos, apenas
estados alcançáveis, mantendo `∅` como estado de erro absorvente. `δ` do
resultado deve ser **total**.

**D2 (6 pts).** `alcancaveis(M)`, `co_alcancaveis(M)`, `remover_inuteis(M)`
(fundindo todos os inúteis em um único estado de erro, preservando totalidade).

**D3 (10 pts).** `minimizar(M) -> AFD` por preenchimento de tabela.
Deve devolver também, opcionalmente, o dicionário `sufixo_distintivo` para cada
par marcado (útil para depurar e para os exercícios de prova).

**D4 (6 pts).** `equivalentes(M1, M2) -> tuple[bool, str | None]` via produto com
`F = XOR` + BFS. O contraexemplo devolvido deve ser o **menor** (BFS garante).

**D5 (5 pts).** `isomorfos(M1, M2) -> bool` — testa se dois AFDs são iguais a
menos de renomeação de estados (percorra os dois em paralelo de `q₀`).

### Testes obrigatórios

`exercicios/aula09/test_conversao.py`:

```python
def test_afd_concorda_com_afn():
    N = AFN_A1                     # o AFN-ε da Parte A1
    M = afn_para_afd(N)
    for w in todas_cadeias({"a","b"}, 8):
        assert N.aceita(w) == M.aceita(w), w

def test_delta_do_afd_e_total():
    M = afn_para_afd(AFN_A1)
    for q in M.Q:
        for a in M.Sigma:
            assert (q, a) in M.delta

def test_minimizar_preserva_linguagem():
    M  = afn_para_afd(AFN_A1)
    Mm = minimizar(M)
    igual, ce = equivalentes(M, Mm)
    assert igual, f"contraexemplo: {ce!r}"

def test_minimizar_e_idempotente():
    Mm = minimizar(afn_para_afd(AFN_A1))
    assert isomorfos(minimizar(Mm), Mm)

def test_minimizar_nunca_cresce():
    M = afn_para_afd(AFN_A1)
    assert len(minimizar(M).Q) <= len(M.Q)

def test_equivalentes_acha_menor_contraexemplo():
    # M1 = termina em 0 ; M2 = termina em 1
    igual, ce = equivalentes(AFD_TERMINA_0, AFD_TERMINA_1)
    assert not igual and len(ce) == 1

def test_unicidade_do_minimo():
    # dois AFDs distintos para a MESMA linguagem minimizam ao mesmo autômato
    assert isomorfos(minimizar(AFD_TERMINA_01_3EST),
                     minimizar(AFD_TERMINA_01_5EST))
```

```bash
uv run pytest exercicios/aula09/ -v
```

---

## Parte E — A explosão exponencial (10 pontos)

**E1 (6 pts).** Escreva `afn_kesimo_do_fim(k) -> AFN` que constrói o AFN de
`Lₖ = { w ∈ {0,1}* | o k-ésimo símbolo do fim é 1 }` com `k+1` estados.

Para `k = 1..12`, preencha e cole em `respostas.md`:

| k | estados AFN | estados AFD | estados AFD mínimo | `2^k` | tempo de conversão |
|---|---|---|---|---|---|

**E2 (4 pts).** Comente:
(a) A coluna "AFD mínimo" é igual a `2^k`? Sempre?
(b) A partir de que `k` a conversão fica lenta na sua máquina?
(c) Por que **Flex** faz essa conversão de todo modo, enquanto o motor de regex
do Go (RE2) usa **DFA lazy**? Explique o trade-off em 5 linhas.

---

## Parte F — Desafio bônus (+10 pontos)

**F1.** Implemente a **minimização de Hopcroft** (`O(|Q|·|Σ|·log|Q|)`) por
refinamento de partições:

```
P ← { F, Q∖F }
W ← { o menor de F, Q∖F }
enquanto W não vazio:
    A ← W.pop()
    para cada a ∈ Σ:
        X ← { q | δ(q,a) ∈ A }
        para cada Y ∈ P com Y ∩ X ≠ ∅ e Y ∖ X ≠ ∅:
            substitua Y por (Y ∩ X) e (Y ∖ X) em P
            atualize W conforme o algoritmo
```

Compare com sua versão de tabela: (a) confirme que produzem AFDs **isomorfos**
para 20 AFDs aleatórios; (b) meça o tempo dos dois para AFDs com
`|Q| = 50, 200, 800` gerados aleatoriamente; (c) plote ou tabele o resultado.

---

## Entrega

```
exercicios/aula09/
├── respostas.md         # Partes A, B, C, E e F
├── conversao.py         # Parte D
├── test_conversao.py    # testes
└── img/                 # (opcional) diagramas Graphviz antes/depois
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus F1** | +10 |
