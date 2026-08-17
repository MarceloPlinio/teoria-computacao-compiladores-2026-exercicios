# Exercício — Aula 11: Equivalência ER ↔ Autômato Finito

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 12 — PR `[Aula 11] Seu Nome`

> ⚠️ Penúltimo componente da **Entrega do Bloco 2**. Ao final desta lista você
> terá um compilador de expressões regulares funcional.

---

## Parte A — Thompson à mão (25 pontos)

Para cada ER, dê: (i) o desenho do AFN-ε, (ii) a tabela `δ` com coluna `ε`,
(iii) a contagem de estados e transições comparada aos limites `2n` e `4n`,
(iv) `E({inicial})`, (v) o trace de uma cadeia aceita e uma rejeitada.

| # | ER | Pts |
|---|---|---|
| A1 | `ab` | 3 |
| A2 | `a\|b` | 3 |
| A3 | `a*` | 3 |
| A4 | `(a\|b)*` | 4 |
| A5 | `(ab)*a` | 5 |
| A6 | `a(b\|c)*d` | 7 |

**Em A4, responda explicitamente:** `ε ∈ L`? Qual das quatro arestas-`ε` do
bloco Kleene garante isso? O que aconteceria se você a omitisse?

---

## Parte B — Eliminação de estados (25 pontos)

**B1 (8 pts).** Converta para ER, mostrando **cada eliminação** com a fórmula
`R(p,s) |= R(p,q)·R(q,q)*·R(q,s)` aplicada:

| `δ` | `0` | `1` |
|---|---|---|
| **→ A** | B | A |
| ***B** | B | A |

**B2 (10 pts).** Idem para:

| `δ` | `a` | `b` |
|---|---|---|
| **→ p** | q | p |
| **q** | q | r |
| ***r** | r | r |

Faça **duas vezes**: eliminando na ordem `q, r` e na ordem `r, q`. Compare o
tamanho das ERs (conte símbolos). Verifique que são equivalentes testando todas
as cadeias de tamanho ≤ 6.

**B3 (7 pts).** Simplifique a melhor ER de B2 usando as identidades da Aula 10.
Documente cada identidade aplicada. Qual a redução percentual?

---

## Parte C — Implementação (35 pontos)

Crie `exercicios/aula11/kleene.py`, importando de `er.py` (Aula 10),
`afn.py` (Aula 08) e `conversao.py` (Aula 09).

**C1 (10 pts).** `thompson(r: ER) -> AFNTh` com os invariantes: um inicial (sem
arestas entrando), um final (sem arestas saindo), `≤ 2n` estados, `≤ 4n`
transições. Inclua um `assert` que **verifica** os invariantes.

**C2 (4 pts).** `para_afn(N: AFNTh, Sigma) -> AFN` — adaptador para a classe da
Aula 08 (nomes de estado como strings).

**C3 (5 pts).** `er_para_afd_minimo(texto, Sigma) -> AFD` — pipeline
`texto → AST → AFN-ε → AFD → mínimo`.

**C4 (12 pts).** `afd_para_er(M) -> str` por eliminação de estados, com a
heurística de eliminar primeiro o estado de menor `(entrada−1)×(saída−1)`.
Deve devolver texto parseável pelo `ParserER`.

**C5 (4 pts).** `tabela_tamanhos(ers, Sigma) -> str` — devolve uma tabela
markdown com as colunas: ER, `|Q|` Thompson, transições Thompson, `|Q|` AFD,
`|Q|` mínimo.

### Testes obrigatórios

`exercicios/aula11/test_kleene.py`:

```python
S = frozenset({"a", "b"})
ERS = ["(a|b)*abb", "a*b*", "(ab)*", "(a|b)*a(a|b)(a|b)", "a?b?", "a+", "∅", "ε"]

def test_invariantes_thompson():
    for e in ERS:
        N = thompson(ParserER(e).parse())
        # nada sai do final, nada entra no inicial
        assert not any(q == N.final for (q, _) in N.delta)
        assert not any(N.inicial in v for v in N.delta.values())

def test_limite_2n_estados():
    r = ParserER("(a|b)*abb").parse()
    N = thompson(r)
    estados = {N.inicial, N.final} | {q for (q, _) in N.delta} \
              | {p for v in N.delta.values() for p in v}
    assert len(estados) == 14

def test_pipeline_concorda_com_linguagem():
    for e in ERS:
        M = er_para_afd_minimo(e, S)
        r = ParserER(e).parse()
        L = linguagem(r, 7)
        for w in todas_cadeias(S, 7):
            assert M.aceita(w) == (w in L), (e, w)

def test_pipeline_concorda_com_re():
    import re
    mapa = {"(a|b)*abb": r"(a|b)*abb", "a*b*": r"a*b*",
            "(ab)*": r"(ab)*", "a+": r"a+", "a?b?": r"a?b?"}
    for e, pat in mapa.items():
        M = er_para_afd_minimo(e, S)
        for w in todas_cadeias(S, 7):
            assert M.aceita(w) == bool(re.fullmatch(pat, w)), (e, w)

def test_afd_minimo_de_abb_tem_4_estados():
    assert len(er_para_afd_minimo("(a|b)*abb", S).Q) == 4

def test_ciclo_completo_er_afd_er():
    for e in ERS:
        M1 = er_para_afd_minimo(e, S)
        e2 = afd_para_er(M1)
        M2 = er_para_afd_minimo(e2, S)
        igual, ce = equivalentes(M1, M2)
        assert igual, f"{e} → {e2}: contraexemplo {ce!r}"

def test_vazio_e_epsilon():
    assert len(linguagem(ParserER("∅").parse(), 5)) == 0
    M = er_para_afd_minimo("ε", S)
    assert M.aceita("") and not M.aceita("a")
```

```bash
uv run pytest exercicios/aula11/ -v
```

---

## Parte D — Análise (15 pontos)

**D1 (5 pts).** Preencha e cole a tabela de C5 para as 8 ERs de `ERS`. Comente:
o AFD mínimo é sempre menor que o de Thompson? Há caso em que o AFD é **maior**?

**D2 (5 pts).** Rode o ciclo `ER → AFD → ER` para as 8 ERs e tabele o tamanho
(em símbolos) da ER original vs. reconstruída. Comente o crescimento. Por que a
eliminação de estados infla tanto?

**D3 (5 pts).** Implemente `scanner_de_ers(padroes: list[tuple[str, str]])` que
recebe `[(nome_token, er)]`, faz a **união dos AFNs de Thompson** guardando em
cada final **qual padrão** ele representa, converte para AFD e tokeniza aplicando
longest match + prioridade (Aula 07).

Teste com:

```python
SC = scanner_de_ers([
    ("IF",  "if"),
    ("ID",  "[a-z][a-z0-9]*"),      # aceite açúcar no seu parser, ou expanda
    ("NUM", "[0-9]+"),
])
assert [t.tipo for t in SC.tokenize("if x1 42")] == ["IF", "ID", "NUM"]
assert SC.tokenize("ifx")[0].tipo == "ID"
```

Explique onde exatamente, no seu código, a **prioridade** é decidida.

---

## Parte E — Desafio bônus (+10 pontos)

**E1 — Pike VM (simulação de AFN sem backtracking).** Implemente
`pike_match(N: AFNTh, w: str) -> bool` que simula o AFN de Thompson mantendo uma
**lista de threads** (conjunto de estados ativos), em `O(|w| · |Q|)` garantido,
sem construir AFD.

Depois:
(a) Compare o tempo com `re.match(r"(a+)+b", "a"*n)` para `n = 20..30`. Mostre
que sua implementação é **linear** enquanto o `re` é exponencial. Cole os números.
(b) Explique por que Pike VM é imune a **ReDoS**.
(c) Estenda para devolver o **lexema casado** (posição final do longest match),
não só um booleano — e mostre que isso é suficiente para um scanner de produção.

---

## Entrega

```
exercicios/aula11/
├── respostas.md        # Partes A, B, D e E
├── kleene.py           # Parte C
├── test_kleene.py      # testes
└── img/                # (opcional) AFNs de Thompson em Graphviz
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus E1** | +10 |
