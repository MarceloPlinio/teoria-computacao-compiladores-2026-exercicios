# Exercício — Aula 10: Expressões Regulares — Fundamentos

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 11 — PR `[Aula 10] Seu Nome`

> ⚠️ O `ParserER` da Parte D é reusado na **Aula 11** (Thompson) e é o
> antepassado do parser do MiniLang (**Aula 32**).

---

## Parte A — Precedência e leitura (20 pontos)

**A1 (8 pts).** Parentize **completamente** e liste as **5 menores** cadeias
de cada ER (em ordem canônica):

| # | ER |
|---|---|
| a | `ab*c` |
| b | `a\|bc*` |
| c | `(a\|b)c*d` |
| d | `a*b\|c` |
| e | `ab\|cd*` |
| f | `a\|b\|c*` |
| g | `(a\|b)*a(a\|b)` |
| h | `0(0\|1)*1` |

**A2 (6 pts).** Para cada ER de A1, diga se `ε ∈ L(r)`. Justifique
**estruturalmente** (regra de nulificabilidade aplicada), não por enumeração.

**A3 (6 pts).** Diga se cada par denota a **mesma** linguagem. Prove com uma
identidade algébrica ou refute com um contraexemplo **explícito**:

| # | Par |
|---|---|
| a | `(ab)*` e `a*b*` |
| b | `(a\|b)*` e `(a*b*)*` |
| c | `a(ba)*` e `(ab)*a` |
| d | `(a*b)*` e `(a\|b)*` |
| e | `∅*` e `ε` |
| f | `(a\|ε)*` e `a*` |
| g | `(a*b*)*` e `(a\|b)*` |
| h | `a*(b\|ε)` e `a*b\|a*` |

---

## Parte B — Escrevendo ERs (25 pontos)

Sobre `Σ = {0, 1}`. Açúcar sintático (`+ ? [ ] { }`) é permitido.

| # | Linguagem | Pts |
|---|---|---|
| B1 | termina em `01` | 2 |
| B2 | contém `101` | 2 |
| B3 | número **par** de `0`s | 3 |
| B4 | exatamente dois `1`s | 2 |
| B5 | **não** contém `00` | 3 |
| B6 | tamanho múltiplo de 3 | 2 |
| B7 | começa e termina com o mesmo símbolo | 3 |
| B8 | todo `0` é imediatamente seguido de `1` | 3 |
| B9 | o **3º símbolo a partir do fim** é `1` | 2 |
| B10 | número par de `0`s **E** número par de `1`s | 3 |

**Para B10**, além da ER, explique a estratégia (dica: pense no AFD de 4 estados
e traduza — ou use a identidade `(00\|11\|(01\|10)(00\|11)*(01\|10))*`).

---

## Parte C — Padrões léxicos (15 pontos)

Escreva ERs (sobre ASCII) e **teste com o módulo `re`** do Python, colando os
casos de teste em `respostas.md`:

| # | Padrão | Pts |
|---|---|---|
| C1 | identificador estilo C (`[A-Za-z_]` seguido de `[A-Za-z0-9_]*`) | 2 |
| C2 | número: inteiro, real, com sinal e expoente opcionais | 4 |
| C3 | literal de string com escapes `\n \t \" \\` | 4 |
| C4 | comentário `/* ... */` — **não** deve casar além do primeiro `*/` | 3 |
| C5 | endereço IPv4 válido (0–255 em cada octeto) | 2 |

Para cada um, dê **3 casos que casam** e **3 que não casam** (armadilhas!).
Em C4, teste explicitamente `/* a */ b /* c */` — quantos casamentos?
Em C5, teste `256.1.1.1` e `1.2.3.04`.

---

## Parte D — Implementação (30 pontos)

Crie `exercicios/aula10/er.py`.

**D1 (6 pts).** AST com `Vazio`, `Epsilon`, `Simbolo`, `Uniao`, `Concat`,
`Estrela` (dataclasses **frozen**, para serem hasheáveis).

**D2 (5 pts).** `linguagem(r, limite) -> set[str]` — `L(r)` truncada.

**D3 (4 pts).** `nulificavel(r) -> bool` — estrutural, sem enumerar.

**D4 (8 pts).** `ParserER` descendente recursivo, com a gramática:

```
uniao   → concat ('|' concat)*
concat  → estrela+
estrela → atomo ('*' | '+' | '?')*
atomo   → '(' uniao ')' | simbolo | 'ε' | '∅'
```

Deve lançar `SyntaxError` com **posição** em: `"("`, `"a|"`, `"*a"`, `"a)"`, `""`.

**D5 (4 pts).** `para_str(r) -> str` — serializa com o **mínimo** de parênteses.

**D6 (3 pts).** `simplificar(r) -> ER` aplicando: `εr → r`, `∅r → ∅`,
`r|∅ → r`, `r|r → r`, `(r*)* → r*`, `∅* → ε`, `ε* → ε`.

### Testes obrigatórios

`exercicios/aula10/test_er.py`:

```python
def test_precedencia_ab_estrela():
    assert linguagem(ParserER("ab*").parse(), 3) == {"a", "ab", "abb"}
    assert linguagem(ParserER("(ab)*").parse(), 4) == {"", "ab", "abab"}

def test_precedencia_uniao():
    assert "" in linguagem(ParserER("a|b*").parse(), 3)      # ε ∈ L(b*)
    assert "" in linguagem(ParserER("(a|b)*").parse(), 3)
    assert "ab" not in linguagem(ParserER("a|b*").parse(), 3)

def test_nulificavel():
    assert nulificavel(ParserER("a*").parse())
    assert nulificavel(ParserER("∅*").parse())        # ∅* = ε
    assert nulificavel(ParserER("a?").parse())
    assert not nulificavel(ParserER("a+").parse())
    assert not nulificavel(ParserER("ab").parse())

def test_identidades(limite=6):
    pares = [("(a*b*)*", "(a|b)*"), ("(a*)*", "a*"), ("∅*", "ε"),
             ("(a|ε)*", "a*"), ("a(ba)*", "(ab)*a"), ("a+", "aa*")]
    for e1, e2 in pares:
        L1 = linguagem(ParserER(e1).parse(), limite)
        L2 = linguagem(ParserER(e2).parse(), limite)
        assert L1 == L2, f"{e1} != {e2}: {L1 ^ L2}"

def test_contraexemplos():
    L1 = linguagem(ParserER("(ab)*").parse(), 4)
    L2 = linguagem(ParserER("a*b*").parse(), 4)
    assert L1 != L2 and "aab" in L2 - L1

def test_roundtrip_para_str():
    for e in ["(a|b)*abb", "a", "ab|c", "a(b|c)", "a*b*", "(ab)*"]:
        r = ParserER(e).parse()
        assert linguagem(ParserER(para_str(r)).parse(), 5) == linguagem(r, 5)

def test_erros_de_sintaxe():
    import pytest
    for ruim in ["(", "a|", "*a", "a)", "", "(a"]:
        with pytest.raises(SyntaxError):
            ParserER(ruim).parse()

def test_simplificar():
    assert simplificar(Concat(Epsilon(), Simbolo("a"))) == Simbolo("a")
    assert simplificar(Concat(Vazio(), Simbolo("a"))) == Vazio()
    assert simplificar(Estrela(Vazio())) == Epsilon()
    assert simplificar(Estrela(Estrela(Simbolo("a")))) == Estrela(Simbolo("a"))
```

```bash
uv run pytest exercicios/aula10/ -v
```

---

## Parte E — Regex de produção e ReDoS (10 pontos)

**E1 (4 pts).** Explique por que `([ab]+)\1` **não** descreve uma linguagem
regular. Qual linguagem ela descreve? Onde ela está na hierarquia de Chomsky
(Aula 04)? Justifique.

**E2 (4 pts).** Meça e tabele o tempo de `re.match(r"(a+)+b", "a"*n)` para
`n = 18, 20, 22, 24, 26`. Confirme o crescimento exponencial (calcule a razão
entre tempos consecutivos). **Não passe de `n=26`** sem timeout.

**E3 (2 pts).** Reescreva o padrão de forma **equivalente e segura** (sem
quantificador aninhado) e mostre o novo tempo para `n = 100000`. Depois pesquise
e cite: (a) o incidente da Cloudflare de 02/07/2019; (b) dois motores de regex
imunes a ReDoS e por quê.

---

## Parte F — Desafio bônus (+10 pontos)

**F1 — Derivadas de Brzozowski.** Implemente casamento de ER **sem** construir
autômato, usando derivadas:

```
δ(r)  = ε se ε ∈ L(r), senão ∅        (nulificabilidade)

D_a(∅)     = ∅
D_a(ε)     = ∅
D_a(b)     = ε se a = b, senão ∅
D_a(r|s)   = D_a(r) | D_a(s)
D_a(rs)    = D_a(r)·s | δ(r)·D_a(s)
D_a(r*)    = D_a(r)·r*
```

Então: `w ∈ L(r)` ⟺ `ε ∈ L(D_{w[n]}(...D_{w[0]}(r)...))`.

(a) Implemente `derivada(r, a) -> ER` e `casa(r, w) -> bool`.
(b) Verifique que concorda com `linguagem()` para 10 ERs e todas as cadeias de
tamanho ≤ 7.
(c) Aplique `simplificar` após cada derivada e mostre que o número de ERs
distintas geradas é **finito** — cada uma delas é um **estado** de um AFD.
Construa esse AFD e compare com o que a Aula 11 produzirá via Thompson.

---

## Entrega

```
exercicios/aula10/
├── respostas.md        # Partes A, B, C, E e F
├── er.py               # Parte D
└── test_er.py          # testes
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus F1** | +10 |
