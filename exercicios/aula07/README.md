# Exercício — Aula 07: Implementando AFDs em Código

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Entrega:** até a véspera da Aula 08 — PR `[Aula 07] Seu Nome`

> ⚠️ **Este exercício é a fundação do scanner do MiniLang (Aula 27).**
> Escreva-o com cuidado: você vai reusá-lo por 30 aulas.

---

## Parte A — As 4 estratégias (25 pontos)

Considere `L = { w ∈ {a,b}* | #ₐ(w) ≡ 0 (mod 3) }`.

Crie `exercicios/aula07/estrategias.py` com **quatro** implementações:

| Função | Estratégia |
|---|---|
| `aceita_ifelif(w)` | `if/elif` explícito |
| `aceita_dict(w)` | dicionário `(estado, símbolo) → estado` |
| `aceita_tabela(w)` | tabela densa `list[list[int]]` indexada por `ord(c)` |
| `aceita_direct(w)` | direct-coded (uma função/rótulo por estado) |

**A1 (12 pts).** As 4 implementações, com type hints e docstrings.

**A2 (5 pts).** `verifica_concordancia(limite)` — confirma que as 4 concordam
para **todas** as cadeias de `{a,b}^{≤limite}`. Devolva a primeira divergência,
se houver.

**A3 (8 pts).** `benchmark(n)` — mede as 4 com uma entrada aleatória de `n`
símbolos (use `time.perf_counter`, tome o **melhor de 5**). Reporte em
`respostas.md` uma tabela com os tempos para `n = 1_000_000` e o *speedup*
relativo à mais lenta. Comente o resultado: a ordem foi a esperada? Por quê?

---

## Parte B — Longest match (25 pontos)

Crie `exercicios/aula07/longest.py` com a classe `AFDParcial` (δ parcial +
`longest_match`).

**B1 (10 pts).** Construa `AFDParcial` para cada padrão:

| Nome | Padrão |
|---|---|
| `INT` | `digito+` |
| `FLOAT` | `digito+ '.' digito+` |
| `ID` | `letra (letra \| digito \| '_')*` |
| `STR` | `'"' (qualquer-exceto-" )* '"'` |
| `HEX` | `'0x' hexdigito+` |

**B2 (8 pts).** Preencha e explique a tabela de resultados de `longest_match`
(posição final e lexema, ou `ERRO`):

| Entrada | `INT` | `FLOAT` | `ID` | `STR` | `HEX` |
|---|---|---|---|---|---|
| `12` | | | | | |
| `12.5` | | | | | |
| `12.` | | | | | |
| `0x1F` | | | | | |
| `0x` | | | | | |
| `"oi"` | | | | | |
| `"oi` | | | | | |
| `_a1` | | | | | |

**B3 (7 pts).** Explique, com o trace do algoritmo, **por que** `12.` devolve
`12` no `FLOAT`... ou não devolve nada. Qual dos dois é o comportamento do seu
código? Qual é o correto para um compilador? Justifique com o que aconteceria
em `x = 12.` e em `for i in 1..10` (uma linguagem com operador `..`).

---

## Parte C — Scanner do MiniLang v0 (35 pontos)

Crie `exercicios/aula07/scanner.py`.

**C1 (8 pts).** `Token` como `dataclass(frozen=True)` com: `tipo`, `lexema`,
`linha`, `coluna`.

**C2 (17 pts).** Classe `Scanner` que tokeniza MiniLang:

| Categoria | Lexemas |
|---|---|
| Palavras-chave | `let`, `while`, `if`, `else`, `print`, `true`, `false` |
| Operadores | `<=`, `>=`, `==`, `!=`, `<`, `>`, `=`, `+`, `-`, `*`, `/`, `%` |
| Delimitadores | `(`, `)`, `{`, `}`, `;`, `,` |
| Literais | `NUM` (inteiro e real), `STR` |
| Identificadores | `ID` |

Requisitos:
- **Longest match** + **prioridade por ordem de declaração**
- Descartar espaços, tabs e `\n` (mas **contando** linhas/colunas)
- Descartar comentários `// ... \n` e `/* ... */`
- Lançar `ErroLexico` com mensagem `"linha L, coluna C: caractere inesperado 'x'"`

**C3 (10 pts).** Testes em `exercicios/aula07/test_scanner.py`:

```python
def test_palavras_chave_vs_id():
    assert [t.tipo for t in Scanner().tokenize("let x = 1;")] == \
           ["LET", "ID", "ASSIGN", "NUM", "SEMI"]
    assert Scanner().tokenize("letx")[0].tipo == "ID"       # longest match
    assert Scanner().tokenize("whilex")[0].tipo == "ID"

def test_operadores_de_dois_caracteres():
    assert [t.tipo for t in Scanner().tokenize("a<=b")] == ["ID","LE","ID"]
    assert [t.tipo for t in Scanner().tokenize("a<b")]  == ["ID","LT","ID"]
    assert [t.tipo for t in Scanner().tokenize("a!=b")] == ["ID","NE","ID"]

def test_comentarios():
    assert len(Scanner().tokenize("x // nada\ny")) == 2
    assert len(Scanner().tokenize("x /* nada\nnada */ y")) == 2

def test_linha_e_coluna():
    ts = Scanner().tokenize("let x\n  = 1;")
    assert (ts[2].linha, ts[2].coluna) == (2, 3)

def test_erro_lexico():
    import pytest
    with pytest.raises(ErroLexico) as e:
        Scanner().tokenize("x = 1 @ 2;")
    assert "coluna" in str(e.value)

def test_programa_completo():
    codigo = open("fixtures/fatorial.ml").read()
    tipos = [t.tipo for t in Scanner().tokenize(codigo)]
    assert tipos[0] == "LET" and tipos[-1] == "SEMI"
```

Crie também `exercicios/aula07/fixtures/fatorial.ml`:

```
// fatorial de n
let n = 10;
let fat = 1;
while (n > 1) {
    fat = fat * n;
    n = n - 1;
}
print fat;
```

```bash
uv run pytest exercicios/aula07/ -v
```

---

## Parte D — Análise (15 pontos)

**D1 (5 pts).** Inverta a ordem de declaração de `LET` e `ID` no seu scanner.
Rode os testes, cole a saída do `pytest` em `respostas.md` e explique
**exatamente** qual regra foi violada.

**D2 (5 pts).** Seu scanner processa `1..10` (dois pontos consecutivos como
operador de faixa)? Se `FLOAT` for `digito+ '.' digito+`, o que `longest_match`
faz com `1..10`? Descreva o problema e proponha **duas** soluções distintas.

**D3 (5 pts).** Meça o throughput do seu scanner (tokens/segundo) num arquivo
de ~100 KB de MiniLang gerado por script. Compare com o `re` do Python fazendo o
mesmo trabalho (`re.finditer` com alternativas nomeadas). Comente a diferença.

---

## Parte E — Desafio bônus (+10 pontos)

**E1.** Escreva `gerar_codigo(afd) -> str` que **emite código Python** para um
reconhecedor *direct-coded* a partir de um `AFDParcial`:

```python
>>> print(gerar_codigo(AFD_MOD3))
def aceita(w):
    i, n = 0, len(w)
    q = 0
    while i < n:
        c = w[i]
        if q == 0:
            if c == 'a': q = 1
            elif c == 'b': q = 0
            else: return False
        elif q == 1:
            ...
        i += 1
    return q in (0,)
```

Depois use `exec()` para carregar o código gerado, verifique que ele concorda
com o AFD original em todas as cadeias de tamanho ≤ 10, e compare a velocidade
com a versão table-driven. Você acabou de escrever um **gerador de scanners**.

---

## Entrega

```
exercicios/aula07/
├── respostas.md         # Partes A3, B2, B3, D e E
├── estrategias.py       # Parte A
├── longest.py           # Parte B
├── scanner.py           # Parte C
├── test_scanner.py      # testes
└── fixtures/fatorial.ml
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / análise | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus E1** | +10 |
