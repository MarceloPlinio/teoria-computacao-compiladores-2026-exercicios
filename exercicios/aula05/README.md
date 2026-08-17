# Exercício — Aula 05: Técnicas de Prova

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 06 — PR `[Aula 05] Seu Nome`

> **Formato obrigatório das provas:** enuncie **BASE**, **HIPÓTESE DE INDUÇÃO** e
> **PASSO INDUTIVO**, marque `[H.I.]` onde a hipótese for usada, e termine com `∎`.
> Provas sem essa estrutura perdem metade dos pontos do item.

---

## Parte A — Indução matemática (25 pontos)

**A1 (5 pts).** `∑_{i=0}^{n} 3ⁱ = (3ⁿ⁺¹ − 1)/2`

**A2 (5 pts).** `n! ≥ 2ⁿ⁻¹` para todo `n ≥ 1`

**A3 (5 pts).** `n³ − n` é divisível por 6, para todo `n ≥ 0`

**A4 (5 pts).** Uma árvore binária com `n` nós internos (cada um com exatamente
2 filhos) tem `n + 1` folhas.

**A5 (5 pts).** Encontre o **erro** na "prova" abaixo e explique exatamente qual
regra da indução foi violada:

> **Afirmação:** todos os cavalos têm a mesma cor.
> **Base:** em um conjunto de 1 cavalo, todos têm a mesma cor. ✅
> **Passo:** dado um conjunto de `k+1` cavalos, remova um: os `k` restantes têm a
> mesma cor [H.I.]. Recoloque-o e remova outro: novamente os `k` têm a mesma cor.
> Logo todos os `k+1` têm a mesma cor. ∎

---

## Parte B — Indução estrutural em cadeias (20 pontos)

Use as definições recursivas:

```
|ε| = 0            |wa| = |w| + 1
εᴿ = ε             (wa)ᴿ = a · wᴿ
w⁰ = ε             wⁿ = w · wⁿ⁻¹
```

**B1 (5 pts).** `|uv| = |u| + |v|` (indução em `|v|`)

**B2 (5 pts).** `(uv)ᴿ = vᴿ uᴿ` (indução em `|v|`)

**B3 (5 pts).** `|wⁿ| = n · |w|` (indução em `n`)

**B4 (5 pts).** Seja `#ₐ(w)` o número de `a`s em `w`. Prove
`#ₐ(uv) = #ₐ(u) + #ₐ(v)` e depois `#ₐ(wᴿ) = #ₐ(w)`.

---

## Parte C — Provando `L(G) = L` (25 pontos)

Para cada gramática, (i) conjecture `L(G)` gerando as 4 menores cadeias,
(ii) prove `L(G) ⊆ L` por indução no **nº de passos de derivação**,
(iii) prove `L ⊆ L(G)` por indução no **tamanho da cadeia**, (iv) conclua.

**C1 (8 pts).** `S → aaSb | ε`

**C2 (8 pts).** `S → aSa | bSb | ε`, sobre `Σ = {a, b}`

**C3 (9 pts).** `S → aS | Sb | ε`, sobre `Σ = {a, b}`.
⚠️ Cuidado: gere as cadeias com código **antes** de conjecturar. A resposta não
é `{aⁿbⁿ}`. Explique por quê, e prove a linguagem correta.

---

## Parte D — Contradição, contraposição e diagonalização (20 pontos)

**D1 (4 pts).** Prove por contradição que `log₂ 3` é irracional.

**D2 (4 pts).** Prove por **contraposição**: se `wᴿ = w` e `|w|` é ímpar, então
`w` tem um símbolo em posição central igual a si mesmo (formule com precisão
antes de provar).

**D3 (4 pts).** Para cada par abaixo, diga se são equivalentes e justifique:

| Original | Candidata |
|---|---|
| Se `L` é regular, então `L` é LLC | Se `L` não é LLC, então `L` não é regular |
| Se `L` é regular, então `L` é LLC | Se `L` é LLC, então `L` é regular |
| Se `G` é tipo 3, então `L(G)` é regular | Se `L(G)` não é regular, então `G` não é tipo 3 |

**D4 (8 pts).** **Diagonalização.**
(a) Escreva com precisão o argumento que mostra que `2^{Σ*}` não é enumerável.
(b) Explique por que o conjunto de **programas Python** é enumerável (descreva a
enumeração).
(c) Conclua formalmente que existe pelo menos uma linguagem sem reconhecedor.
(d) O argumento diz **qual** linguagem é irreconhecível? Comente a diferença
entre uma prova **existencial** e uma prova **construtiva** — e por que a Aula 23
ainda será necessária.

---

## Parte E — Implementação (10 pontos)

Crie `exercicios/aula05/provas.py`.

**E1 (5 pts).** `conjectura_vale(pred_esq, pred_dir, sigma, limite)` → devolve
`(True, None)` ou `(False, contraexemplo)`, buscando em ordem canônica (o
contraexemplo devolvido deve ser o **menor** possível).

**E2 (5 pts).** `verifica_gramatica(G, pred, tam_max)` → gera `L(G)` por BFS
(reuse o código da Aula 03) e devolve:

```python
{
  "gerados_fora_de_L": [...],   # testemunhas de que L(G) ⊄ L
  "de_L_nao_gerados": [...],    # testemunhas de que L ⊄ L(G)
  "iguais_ate_limite": bool,
}
```

Use-a para **falsificar antes de provar** as gramáticas de C1–C3.

### Testes obrigatórios

`exercicios/aula05/test_provas.py`:

```python
def test_acha_menor_contraexemplo():
    ok, ce = conjectura_vale(lambda w: len(w) % 2 == 0,
                             lambda w: w.count("a") % 2 == 0,
                             {"a", "b"}, 6)
    assert not ok and len(ce) == 2          # 'ab' ou 'ba'

def test_conjectura_verdadeira():
    ok, ce = conjectura_vale(lambda w: w.count("a") % 2 == 0,
                             lambda w: w[::-1].count("a") % 2 == 0,
                             {"a", "b"}, 8)
    assert ok and ce is None

def test_verifica_anbn():
    r = verifica_gramatica({"S": ["aSb", ""]},
                           lambda w: w == "a"*(len(w)//2) + "b"*(len(w)//2)
                                      and len(w) % 2 == 0, 8)
    assert r["iguais_ate_limite"]

def test_detecta_gramatica_errada():
    # S → aS | Sb | ε  NÃO gera apenas {a^n b^n}
    r = verifica_gramatica({"S": ["aS", "Sb", ""]},
                           lambda w: w == "a"*(len(w)//2) + "b"*(len(w)//2)
                                      and len(w) % 2 == 0, 6)
    assert r["gerados_fora_de_L"]
```

```bash
uv run pytest exercicios/aula05/ -v
```

---

## Parte F — Desafio bônus (+10 pontos)

**F1.** O **Teorema de Cantor** diz que `|2^A| > |A|` para qualquer conjunto `A`.
Prove-o por diagonalização: suponha uma bijeção `f: A → 2^A` e construa
`D = { x ∈ A | x ∉ f(x) }`. Mostre que `D` não está na imagem de `f`.
Depois responda: qual a relação entre esse `D` e o **paradoxo de Russell**?
E entre ele e o programa que a Aula 23 construirá para o Problema da Parada?

---

## Entrega

```
exercicios/aula05/
├── respostas.md        # Partes A–D e F
├── provas.py           # Parte E
└── test_provas.py      # testes
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova (estrutura BASE/H.I./PASSO) | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus F1** | +10 |
