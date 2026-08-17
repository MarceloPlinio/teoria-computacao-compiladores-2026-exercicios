# Exercício — Aula 06: Autômato Finito Determinístico (AFD)

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 07 — PR `[Aula 06] Seu Nome`

---

## Parte A — Lendo AFDs (20 pontos)

Considere `M₁`:

| `δ` | `0` | `1` |
|---|---|---|
| **→ A** | B | A |
| **B** | C | A |
| ***C** | C | A |

**A1 (5 pts).** Rastreie, configuração por configuração, e diga se aceita:
`00`, `010`, `0100`, `1000`, `ε`, `1010`.

**A2 (5 pts).** Descreva `L(M₁)` em português **e** na notação `{ w | ... }`.

**A3 (5 pts).** Nomeie cada estado com o seu **significado**. Justifique por que
`C` tem um laço em `0`.

**A4 (5 pts).** Construa `M₁'` que aceita o **complemento** de `L(M₁)`.
Verifique com 4 cadeias. Por que a inversão de `F` é válida aqui?

---

## Parte B — Projetando AFDs (35 pontos)

Para cada linguagem: (i) escreva o **significado de cada estado** antes de
desenhar, (ii) dê o **diagrama** (ASCII ou imagem), (iii) dê a **tabela de
transição** completa (com estado de erro se necessário), (iv) teste com 3 cadeias
aceitas e 3 rejeitadas.

`Σ = {0, 1}`, salvo indicação.

| # | Linguagem | Pts |
|---|---|---|
| B1 | cadeias que terminam com `010` | 4 |
| B2 | cadeias que contêm **pelo menos** dois `0`s e **no máximo** um `1` | 5 |
| B3 | `#₀(w)` par **e** `#₁(w) ≡ 0 (mod 3)` (use produto de estados) | 5 |
| B4 | cadeias que **não** contêm a subcadeia `101` | 5 |
| B5 | cadeias que, em binário, são divisíveis por **5** | 6 |
| B6 | sobre `Σ = {a,b,c}`: cadeias em que `a`, `b` e `c` aparecem ao menos uma vez | 5 |
| B7 | cadeias de tamanho par cujo símbolo do meio... **explique por que é impossível** | 5 |

Em **B7**, a linguagem é `{ w | |w| par, e o símbolo na posição |w|/2 é 0 }`.
Argumente (sem prova formal ainda) por que nenhum AFD a reconhece.

---

## Parte C — Formalização (15 pontos)

**C1 (5 pts).** Escreva a quíntupla `(Q, Σ, δ, q₀, F)` **completa** do seu AFD de
B1, com `δ` listada par por par.

**C2 (5 pts).** Usando a definição recursiva de `δ̂`, calcule passo a passo
`δ̂(q₀, 01010)` para o AFD de B1. Mostre cada aplicação da recursão.

**C3 (5 pts).** Prove por **indução em `|w|`** que, no AFD de contagem módulo 3
(Padrão 2 da aula), `δ̂(r0, w) = r_j` onde `j = #ₐ(w) mod 3`.
Use BASE / H.I. / PASSO.

---

## Parte D — Implementação (30 pontos)

Crie `exercicios/aula06/afd.py` reusando a classe `AFD` da aula (copie e estenda).

**D1 (8 pts).** Codifique os AFDs de **B1, B3, B4 e B5** como constantes do
módulo (`AFD_B1`, `AFD_B3`, ...). O `__post_init__` deve validar que `δ` é total.

**D2 (14 pts).** Implemente:

| Função | Descrição |
|---|---|
| `linguagem_ate(M, limite)` | cadeias aceitas de tamanho ≤ `limite`, em ordem canônica |
| `eh_vazia(M)` | `True` se `L(M) = ∅` (BFS de alcançabilidade a partir de `q₀`) |
| `menor_aceita(M)` | menor cadeia aceita, ou `None` |
| `eh_universal(M)` | `True` se `L(M) = Σ*` (dica: `eh_vazia(complemento)`) |
| `estados_alcancaveis(M)` | conjunto de estados alcançáveis de `q₀` |
| `estados_uteis(M)` | estados alcançáveis **e** que alcançam algum final |
| `para_dot(M)` | string Graphviz, com arestas paralelas agrupadas |

**D3 (8 pts).** Implemente `equivalentes_ate(M1, M2, limite) -> tuple[bool, str|None]`:
compara `L(M1)` e `L(M2)` em `Σ^{≤limite}` e devolve o **menor** contraexemplo se
diferirem. Use-a para conferir que seu AFD de B4 é o complemento correto do AFD
que aceita "contém `101`".

### Testes obrigatórios

`exercicios/aula06/test_afd.py` — mínimo **4 asserções por AFD** e uma por função:

```python
def test_b5_divisivel_por_5():
    for n in range(0, 40):
        b = bin(n)[2:]
        assert AFD_B5.aceita(b) == (n % 5 == 0), f"falhou em {n} ({b})"

def test_delta_total_obrigatoria():
    import pytest
    with pytest.raises(AssertionError):
        AFD(frozenset({"q"}), frozenset({"a","b"}),
            {("q","a"): "q"}, "q", frozenset({"q"}))   # falta (q,b)

def test_complemento_e_involucao():
    assert linguagem_ate(AFD_B1.complemento().complemento(), 5) == \
           linguagem_ate(AFD_B1, 5)

def test_vazia_e_universal():
    assert eh_vazia(AFD(frozenset({"q"}), frozenset({"0","1"}),
                        {("q","0"):"q", ("q","1"):"q"}, "q", frozenset()))
    assert eh_universal(AFD(frozenset({"q"}), frozenset({"0","1"}),
                        {("q","0"):"q", ("q","1"):"q"}, "q", frozenset({"q"})))
```

```bash
uv run pytest exercicios/aula06/ -v
```

---

## Parte E — Desafio bônus (+10 pontos)

**E1.** Escreva `afd_divisivel_por(k, base)` que **constrói automaticamente** o
AFD que aceita representações na `base` dada divisíveis por `k`
(estados = restos, transição `r → (base·r + d) mod k`).

Teste para `k = 1..12` e `base ∈ {2, 10}`, comparando com `int(w, base) % k == 0`
para todas as cadeias de tamanho ≤ 6.

Depois responda: quantos estados o AFD tem? Esse número é **mínimo**? (Teste
`k = 4` na base 2 e conte os estados realmente distinguíveis — voltaremos a isso
na Aula 09.)

---

## Entrega

```
exercicios/aula06/
├── respostas.md        # Partes A, B, C e E (diagramas em ASCII ou imagens)
├── afd.py              # Parte D
├── test_afd.py         # testes
└── img/                # (opcional) diagramas gerados com Graphviz
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus E1** | +10 |
