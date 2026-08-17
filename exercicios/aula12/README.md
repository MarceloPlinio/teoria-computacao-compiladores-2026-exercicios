# Exercício — Aula 12: Gramáticas Regulares, Fechamento e Bombeamento

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 13 — PR `[Aula 12] Seu Nome`

> 🏆 **Esta aula fecha o Bloco 2.** Além da lista, entregue o pacote `automata/`
> (Parte F) num PR separado: `[Bloco 2] Seu Nome`.

---

## Parte A — Gramáticas Regulares (15 pontos)

**A1 (5 pts).** Converta para AFN, depois para AFD, e diga qual é `L(G)`:

```
S → 0S | 1A | ε
A → 0A | 1S
```

**A2 (5 pts).** Converta este AFD para gramática regular linear à **direita**:

| `δ` | `a` | `b` |
|---|---|---|
| **→ p** | q | p |
| ***q** | q | r |
| **r** | p | r |

**A3 (5 pts).** Escreva a mesma linguagem de A2 com uma gramática linear à
**esquerda**. Depois explique por que **misturar** as duas orientações na mesma
gramática pode gerar uma linguagem **não regular** — dê um exemplo concreto de
gramática mista que gera `{aⁿbⁿ}`.

---

## Parte B — Fechamento e produto (25 pontos)

Sejam, sobre `Σ = {a, b}`:
`L₁ = { w | #ₐ(w) é par }` e `L₂ = { w | w termina em b }`.

**B1 (5 pts).** Dê os AFDs mínimos de `L₁` e `L₂` (2 estados cada).

**B2 (10 pts).** Construa o **produto** e dê a tabela completa (4 estados) para:
(a) `L₁ ∩ L₂`  (b) `L₁ ∪ L₂`  (c) `L₁ − L₂`  (d) diferença simétrica.
Minimize cada um e diga quantos estados sobraram.

**B3 (5 pts).** Dê um contraexemplo concreto (AFN com ≤ 3 estados) mostrando que
**inverter `F` de um AFN não produz o complemento**. Exiba uma cadeia aceita
pelos dois autômatos.

**B4 (5 pts).** Prove que as regulares são fechadas sob **reverso**: descreva a
construção e argumente por que ela é correta. Aplique-a ao AFD de A2 e verifique
com 4 cadeias.

---

## Parte C — Lema do Bombeamento (30 pontos)

Para cada linguagem, dê a prova **completa** no formato de 6 passos, indicando
explicitamente **quem escolhe** `p`, `w`, a decomposição `xyz` e `i`. Trate
**todas** as decomposições permitidas por `|xy| ≤ p`.

| # | Linguagem | Pts |
|---|---|---|
| C1 | `{ 0ⁿ1ⁿ \| n ≥ 0 }` | 4 |
| C2 | `{ w ∈ {a,b}* \| w = wᴿ }` | 5 |
| C3 | `{ aⁿbᵐ \| n > m ≥ 0 }` | 5 |
| C4 | `{ ww \| w ∈ {a,b}* }` | 5 |
| C5 | `{ aⁿ \| n é um quadrado perfeito }` | 6 |
| C6 | `{ aⁿbⁿcⁿ \| n ≥ 0 }` | 5 |

**Em C5**, você precisará de `i` grande e do argumento das **lacunas**:
`(m+1)² − m² = 2m+1`, que cresce sem limite.

---

## Parte D — Fechamento como atalho (15 pontos)

Prove **sem bombear diretamente**, usando apenas propriedades de fechamento e o
catálogo de linguagens não regulares já conhecidas:

**D1 (5 pts).** `{ w ∈ {a,b}* | #ₐ(w) ≠ #_b(w) }`

**D2 (5 pts).** `{ aⁱbʲ | i ≠ j }`
*(Atenção: por que a interseção com `a*b*` é necessária?)*

**D3 (5 pts).** `{ w ∈ {a,b,c}* | #ₐ(w) = #_b(w) = #_c(w) }`

---

## Parte E — A armadilha (10 pontos)

**E1 (5 pts).** Considere `L = { aⁱbʲcᵏ | i = 0 ou j = k }`.

(a) Mostre que `L` **satisfaz** o Lema do Bombeamento: para `p = 1`, exiba a
decomposição que funciona em cada caso.
(b) Prove que `L` **não é regular** (use Myhill-Nerode ou fechamento).
(c) Conclua: qual afirmação sobre o lema esse exemplo refuta? Escreva-a
precisamente.

**E2 (5 pts).** Analise `L = { w ∈ {0,1}* | w tem o mesmo número de ocorrências
de 01 e de 10 }`. Ela é regular? **Prove sua resposta.**
*(Dica: pense no primeiro e no último símbolo de `w`. A resposta pode surpreender.)*

---

## Parte F — 🏆 ENTREGA DO BLOCO 2: pacote `automata/` (peso separado)

Consolide as Aulas 06–12 em um pacote instalável.

### Estrutura exigida

```
automata/
├── __init__.py
├── __main__.py           # CLI
├── afd.py                # AFD, δ̂, complemento, dot, alcancaveis
├── afn.py                # AFN-ε, fecho_eps, mover, construções composicionais
├── er.py                 # AST de ER, ParserER, linguagem, simplificar
├── conversao.py          # afn_para_afd, minimizar, equivalentes, isomorfos
├── kleene.py             # thompson, afd_para_er, er_para_afd_minimo
├── fechamento.py         # produto, reverso, homomorfismo
├── gramatica.py          # gr_para_afn, afn_para_gr
└── README.md             # exemplos de uso
tests/
└── test_*.py             # cobertura >= 90%
```

### CLI obrigatório

```bash
uv run python -m automata er     "(a|b)*abb" --minimizar --dot saida.dot
uv run python -m automata testar "(a|b)*abb" abb aabb ab ""
uv run python -m automata equiv  "(a|b)*abb" "(a|b)*a(a|b)b"
uv run python -m automata inter  "(a|b)*a" "b(a|b)*" --dot inter.dot
uv run python -m automata minimizar --dot-in entrada.dot --dot-out min.dot
uv run python -m automata gramatica "(a|b)*abb"       # imprime a GR equivalente
```

### Critérios de aceitação

| Item | Verificação |
|---|---|
| `pytest` verde | `uv run pytest -v` |
| Cobertura ≥ 90% | `uv run pytest --cov=automata --cov-report=term-missing` |
| `δ` sempre total nos AFDs | assert em `__post_init__` |
| Pipeline consistente | ER ↔ AFN ↔ AFD ↔ mínimo ↔ GR concordam em `Σ^{≤8}` |
| Sem regressões | testes das Aulas 06–11 continuam passando |
| `--dot` gera arquivo válido | `dot -Tpng saida.dot -o /dev/null` sem erro |
| README com 6 exemplos rodáveis | copiar/colar funciona |

### Testes de integração exigidos

```python
def test_pipeline_completo_consistente():
    S = frozenset({"a", "b"})
    for e in ["(a|b)*abb", "a*b*", "(ab)*", "a?b+", "(a|b)*a(a|b)(a|b)"]:
        M  = er_para_afd_minimo(e, S)
        G  = afn_para_gr(para_afn(thompson(ParserER(e).parse()), S))
        N2 = gr_para_afn(G)
        M2 = minimizar(afn_para_afd(N2))
        igual, ce = equivalentes(M, M2)
        assert igual, f"{e}: contraexemplo {ce!r}"

def test_de_morgan():
    S = frozenset({"a", "b"})
    A = er_para_afd_minimo("(a|b)*abb", S)
    B = er_para_afd_minimo("a*b*", S)
    esq = produto(A, B, "inter").complemento()
    dir = produto(A.complemento(), B.complemento(), "uniao")
    assert equivalentes(esq, dir)[0]

def test_reverso_e_involucao():
    S = frozenset({"a", "b"})
    A = er_para_afd_minimo("ab*a", S)
    R = minimizar(afn_para_afd(reverso(A)))
    RR = minimizar(afn_para_afd(reverso(R)))
    assert equivalentes(A, RR)[0]
```

---

## Parte G — Desafio bônus (+10 pontos)

**G1.** Implemente `nao_bombeavel(pertence, p_max, tam_max)` que **busca**
violações do Lema do Bombeamento para um predicado `pertence(w) -> bool`:

para cada `p` de 1 a `p_max`, procura uma cadeia `w ∈ L` com `|w| ≥ p` tal que
**toda** decomposição `w = xyz` com `|y| ≥ 1, |xy| ≤ p` admite algum `i` com
`xyⁱz ∉ L`. Devolve `(p, w, i)` da menor testemunha encontrada.

Rode em:
(a) `{aⁿbⁿ}` — deve achar testemunha
(b) `{aⁿ | n primo}` — deve achar (mas precisa de `i` grande; comente o custo)
(c) `{aⁱbʲcᵏ | i=0 ou j=k}` — **não** deve achar
(d) `(a|b)*abb` — **não** deve achar (é regular)

Escreva em `respostas.md`: por que (c) e (d) dão o mesmo resultado da ferramenta
mas conclusões **opostas** sobre regularidade? O que isso ensina sobre os limites
de verificação empírica?

---

## Entrega

```
exercicios/aula12/
├── respostas.md        # Partes A–E e G
├── fechamento.py       # produto, reverso, homomorfismo
├── gramatica_reg.py    # gr_para_afn, afn_para_gr
├── bombeamento.py      # Parte G
└── test_*.py           # testes
```

E, em **PR separado** (`[Bloco 2] Seu Nome`):

```
automata/               # pacote consolidado (Parte F)
tests/
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova (formato de 6 passos) | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus G1** | +10 |
| **Entrega do Bloco 2** | avaliada separadamente (20% junto com Blocos 3 e 4) |
