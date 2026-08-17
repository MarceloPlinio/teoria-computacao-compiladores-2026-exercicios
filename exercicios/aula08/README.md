# Exercício — Aula 08: Autômato Finito Não-Determinístico

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 09 — PR `[Aula 08] Seu Nome`

> ⚠️ As funções `uniao`, `concat`, `kleene` da Parte C são reusadas na
> **Aula 11** (construção de Thompson). Escreva-as com cuidado.

---

## Parte A — Rastreando AFNs (20 pontos)

AFN-ε `N₁` sobre `Σ = {a, b}`:

| `δ` | `a` | `b` | `ε` |
|---|---|---|---|
| **→ p0** | {p0, p1} | {p0} | {p2} |
| **p1** | ∅ | {p3} | ∅ |
| **p2** | {p2} | ∅ | ∅ |
| ***p3** | {p3} | {p3} | ∅ |

**A1 (5 pts).** Calcule `E({p0})`, `E({p1})`, `E({p0,p3})`.

**A2 (8 pts).** Rastreie o **conjunto de estados ativos** passo a passo (uma
linha por símbolo, mostrando `mover` e depois `fecho`) e diga aceita/rejeita:
`ε`, `ab`, `aab`, `ba`, `abba`, `aabb`.

**A3 (4 pts).** Descreva `L(N₁)` em português e na notação `{ w | ... }`.

**A4 (3 pts).** Liste **todos** os conjuntos de estados distintos que
apareceram. Quantos são? Compare com `2^|Q| = 16` e comente.

---

## Parte B — Projetando AFNs (30 pontos)

Para cada linguagem: (i) desenhe o AFN (ASCII ou imagem), (ii) dê a tabela `δ`
(com coluna `ε`), (iii) conte os estados, (iv) **estime** o tamanho do AFD
mínimo equivalente e justifique.

| # | Linguagem sobre `Σ = {0,1}` | Pts |
|---|---|---|
| B1 | contém `011` **ou** `110` | 5 |
| B2 | `(01)* ∪ (10)*` | 5 |
| B3 | o **4º símbolo a partir do fim** é `1` | 6 |
| B4 | contém `0` **e** contém `1` | 4 |
| B5 | `{ w \| w = xy, x ∈ (01)*, y ∈ 1* }` | 5 |
| B6 | `{ w \| \|w\| ≡ 0 mod 2 } ∪ { w \| \|w\| ≡ 0 mod 3 }` | 5 |

**B3 generalizado (obrigatório):** para "o `k`-ésimo símbolo do fim é `1`", dê
o número de estados do AFN e do AFD mínimo em função de `k`. Prove
informalmente a cota do AFD (dica: o AFD precisa lembrar os últimos `k` símbolos
— quantas configurações distintas existem?).

---

## Parte C — Implementação (35 pontos)

Crie `exercicios/aula08/afn.py` com a classe `AFN` (copie da aula e estenda).

**C1 (8 pts).** Métodos: `mover`, `fecho_eps`, `delta_hat`, `aceita`, `trace`.
`trace` devolve a lista de conjuntos de estados ativos.

**C2 (6 pts).** Codifique **B1, B3 (k=4) e B4** como constantes do módulo.

**C3 (14 pts).** Construções composicionais. Todas devem **renomear estados**
(prefixo ou contador global) para evitar colisão, e devolver um `AFN` válido:

| Função | `L` resultante |
|---|---|
| `vazio(Sigma)` | `∅` |
| `epsilon(Sigma)` | `{ε}` |
| `literal(a, Sigma)` | `{a}` |
| `uniao(N1, N2)` | `L(N1) ∪ L(N2)` |
| `concat(N1, N2)` | `L(N1) · L(N2)` |
| `kleene(N)` | `L(N)*` |
| `positivo(N)` | `L(N)⁺` |
| `opcional(N)` | `L(N) ∪ {ε}` |

**C4 (7 pts).** `caminhos(N, w) -> list[list[str]]` — **todos** os caminhos
(sequências de estados, incluindo saltos-`ε`) que consomem `w` inteira.

### Testes obrigatórios

`exercicios/aula08/test_afn.py`:

```python
S = frozenset({"a", "b"})

def test_fecho_eps_inicial_importa():
    # q0 --ε--> q1(final);  aceita ε SOMENTE com fecho inicial
    N = AFN(frozenset({"q0","q1"}), S,
            {("q0", ""): frozenset({"q1"})}, "q0", frozenset({"q1"}))
    assert N.aceita("")

def test_ordem_move_depois_fecho():
    N = AFN(frozenset({"q0","q1","q2"}), S,
            {("q0","a"): frozenset({"q1"}), ("q1",""): frozenset({"q2"})},
            "q0", frozenset({"q2"}))
    assert N.aceita("a") and not N.aceita("")

def test_composicao_ab_estrela():
    M = kleene(concat(literal("a", S), literal("b", S)))
    for w in ["", "ab", "abab", "ababab"]:
        assert M.aceita(w), w
    for w in ["a", "b", "ba", "aba", "abb"]:
        assert not M.aceita(w), w

def test_uniao_e_vazio():
    assert not vazio(S).aceita("") and not vazio(S).aceita("a")
    U = uniao(literal("a", S), literal("b", S))
    assert U.aceita("a") and U.aceita("b") and not U.aceita("ab")

def test_kleene_de_epsilon_nao_trava():
    assert kleene(epsilon(S)).aceita("")          # não deve entrar em loop

def test_b3_quarto_do_fim():
    for w in ["1000", "01000", "1111", "0001000"]:
        assert AFN_B3.aceita(w), w
    for w in ["", "1", "0000", "0100"]:
        assert not AFN_B3.aceita(w), w

def test_caminhos_conta():
    assert len(caminhos(AFN_B1, "011")) >= 1
```

```bash
uv run pytest exercicios/aula08/ -v
```

---

## Parte D — Análise (15 pontos)

**D1 (5 pts).** Rode `caminhos(AFN_B1, w)` para `w` aleatório de tamanho
`4, 6, 8, 10, 12`. Tabele o número de caminhos. O crescimento é polinomial ou
exponencial? Compare com o custo de `aceita` (simulação por conjunto). Explique
por que a simulação por conjunto **não** sofre essa explosão.

**D2 (5 pts).** Implemente `aceita_backtracking(N, w)` (busca em profundidade
com retrocesso, sem conjunto de estados) e meça o tempo das duas abordagens em
`AFN_B3` com `k=12` e cadeias de 24 símbolos. Cole os números.

**D3 (5 pts).** Pesquise **ReDoS** (*regex denial of service*). Explique, usando
o que você mediu em D2, por que o padrão `(a+)+b` aplicado a `"aaaaaaaaaaaaaaaaaaaaaaaaaaX"`
trava um motor com backtracking mas não um baseado em autômato. Cite uma
linguagem/biblioteca de cada tipo.

---

## Parte E — Desafio bônus (+10 pontos)

**E1.** Prove que o AFD mínimo para
`Lₖ = { w ∈ {0,1}* | o k-ésimo símbolo do fim de w é 1 }` tem **exatamente**
`2^k` estados.

Estratégia: mostre que quaisquer duas cadeias distintas `x, y ∈ {0,1}^k` são
**distinguíveis** — exiba um sufixo `z` tal que exatamente uma de `xz`, `yz`
está em `Lₖ`. Conclua pelo princípio de que estados distinguíveis não podem ser
fundidos (formalizaremos como **Myhill-Nerode** na Aula 09).

Depois, verifique computacionalmente para `k = 1..8`: converta o AFN
(`AFN_B3` generalizado) para AFD, minimize, e conte os estados.
*(Use a implementação da Aula 09 quando ela existir; por ora, conte os conjuntos
de estados alcançáveis na simulação.)*

---

## Entrega

```
exercicios/aula08/
├── respostas.md        # Partes A, B, D e E
├── afn.py              # Parte C
└── test_afn.py         # testes
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus E1** | +10 |
