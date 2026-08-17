# Exercício — Aula 01: Introdução à Teoria da Computação e aos Compiladores

**Disciplina:** Teoria da Computação e Compiladores — UNIFG 2026/2
**Professor:** Petros Barreto
**Entrega:** até a véspera da Aula 02, via Pull Request `[Aula 01] Seu Nome`

---

## Parte A — Conceitual (40 pontos)

**A1 (8 pts).** Explique, com suas palavras e um exemplo próprio, a diferença entre
um **sistema gerador** e um **sistema reconhecedor** de linguagens. Dê uma gramática
e o esboço de um reconhecedor para a *mesma* linguagem.

**A2 (8 pts).** Para cada linguagem, indique o recurso mínimo de memória do
reconhecedor (*nenhum além do estado* / *pilha* / *memória ilimitada*) e **justifique
em uma frase**:

| # | Linguagem sobre `Σ = {a, b}` |
|---|---|
| a | cadeias que começam com `a` |
| b | cadeias com número igual de `a`s e `b`s |
| c | cadeias de tamanho múltiplo de 3 |
| d | palíndromos |
| e | `{ aⁿbⁿcⁿ \| n ≥ 1 }` |

**A3 (8 pts).** Desenhe (ASCII ou imagem) o pipeline de compilação para a instrução
abaixo, mostrando a saída de **cada uma das 6 fases** vistas em aula:

```c
total = preco * 2 + 5;
```

**A4 (8 pts).** Uma equipe quer suportar 4 linguagens-fonte em 5 arquiteturas.
Quantos tradutores completos são necessários **com** e **sem** uma representação
intermediária? Explique por que o LLVM adota a segunda estratégia.

**A5 (8 pts).** Classifique cada ferramenta como *compilador*, *interpretador* ou
*híbrido*, justificando: `gcc`, `CPython`, `javac` + JVM, `tsc` (TypeScript),
V8 (JavaScript), `rustc`.

---

## Parte B — Tokenização manual (20 pontos)

**B1 (10 pts).** Tokenize o programa abaixo no formato `<TIPO, lexema>`, uma linha
por token, descartando espaços e comentários:

```c
// calcula desconto
while (qtd <= 100) {
    preco = preco - 0.5;
    qtd = qtd + 1;
}
```

**B2 (5 pts).** Qual o problema de tokenizar `a<=-1` sem a regra do **maior
casamento possível** (*longest match*)? Mostre as duas tokenizações possíveis.

**B3 (5 pts).** O scanner consegue detectar o erro em `x = = 5;`? E em
`y = z + 1;` onde `z` nunca foi declarado? Explique **qual fase** pega cada erro.

---

## Parte C — Implementação (30 pontos)

Crie o arquivo `exercicios/aula01/reconhecedores.py`. Nenhuma biblioteca externa.

**C1 (7 pts).** `reconhece_abc(cadeia)` → aceita `L = { aⁿbⁿcⁿ | n ≥ 0 }`.

**C2 (7 pts).** `balanceado(cadeia)` → aceita cadeias com `()`, `[]`, `{}`
corretamente aninhados (ignore outros caracteres).

**C3 (8 pts).** `palindromo(cadeia)` → aceita palíndromos sobre `{a, b}`.
**Restrição:** proibido usar `cadeia[::-1]`, `reversed()` ou `list.reverse()`.
Use dois índices convergentes.

**C4 (8 pts).** `tokenize(codigo)` → recebe uma string e devolve uma lista de
tuplas `(tipo, lexema)`, implementando as regras da Parte B (palavras-chave,
identificadores, números, operadores de 1 e 2 caracteres, delimitadores).
Deve aplicar *longest match* e lançar `ValueError` em caractere inválido.

### Testes obrigatórios

Crie `exercicios/aula01/test_reconhecedores.py` com **no mínimo 4 asserções por
função** (casos válidos, inválidos, vazio e borda):

```python
from reconhecedores import reconhece_abc, balanceado, palindromo, tokenize

def test_abc():
    assert reconhece_abc("")
    assert reconhece_abc("aaabbbccc")
    assert not reconhece_abc("aabbc")
    assert not reconhece_abc("abcabc")

def test_tokenize():
    assert tokenize("x = 1;") == [
        ("ID", "x"), ("ASSIGN", "="), ("NUM", "1"), ("SEMI", ";"),
    ]
    assert tokenize("a<=-1")[1] == ("LE", "<=")
```

Rode com:

```bash
uv run pytest exercicios/aula01/ -v
```

---

## Parte D — Desafio bônus (+10 pontos)

**D1.** Explique por que a linguagem *"cadeias `w` que são programas Python que
terminam sua execução"* **não** pode ser reconhecida por nenhum programa —
mesmo com memória infinita. Não precisa de prova formal; construa um argumento
por contradição em ~10 linhas. (Voltaremos a isso na Aula 23.)

---

## Entrega

```
exercicios/aula01/
├── respostas.md                  # Partes A, B e D
├── reconhecedores.py             # Parte C
└── test_reconhecedores.py        # testes da Parte C
```

## Rubrica

| Critério | Pontos |
|---|---|
| Corretude formal | 40 |
| Justificativa / prova | 25 |
| Implementação e testes | 25 |
| Clareza e organização | 10 |
| **Bônus D1** | +10 |
