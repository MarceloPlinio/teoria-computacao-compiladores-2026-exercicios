# 🛠️ Projeto MiniLang — Especificação

**UC:** Teoria da Computação e Compiladores (`0022028`) — UNIFG 2026/2
**Professor:** Petros Barreto
**Peso:** 30% da média final
**Entrega final:** Aula 40 (apresentação de 15 min + relatório)

---

## 🎯 O que você vai construir

Um **compilador completo** para MiniLang, uma linguagem imperativa pequena,
implementado em **Python 3.13** e composto de seis estágios:

```
   programa.ml
        │
        ▼
┌───────────────────┐
│ 1. SCANNER        │  texto → tokens              Aula 27
│    (AFD)          │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ 2. PARSER         │  tokens → AST                Aula 32
│    (recursivo +   │
│     Pratt)        │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ 3. SEMÂNTICA      │  AST → AST anotada           Aula 35
│    (escopos +     │  + tabela de símbolos
│     tipos)        │
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ 4. IR (TAC)       │  AST → código de 3 endereços Aula 36
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ 5. OTIMIZAÇÃO     │  TAC → TAC (opcional, bônus) Aula 38
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ 6. VM DE PILHA    │  TAC → bytecode → execução   Aula 37
└───────────────────┘
```

---

## 📜 A linguagem MiniLang

### Programa de exemplo

```
// fatorial iterativo
let n: int = 10;
let fat: int = 1;

while (n > 1) {
    fat = fat * n;
    n = n - 1;
}

print fat;          // 3628800
```

```
// condicional e booleanos
let idade: int = 20;
let maior: bool = idade >= 18;

if (maior) {
    print 1;
} else {
    print 0;
}
```

```
// funções (nível 3 — bônus)
fn dobro(x: int): int {
    return x * 2;
}

print dobro(21);    // 42
```

---

## 📐 Gramática de referência (EBNF)

```ebnf
programa   = { declaracao } ;

declaracao = decl_var
           | decl_fn
           | comando ;

decl_var   = "let" ID [ ":" tipo ] "=" expr ";" ;
decl_fn    = "fn" ID "(" [ params ] ")" [ ":" tipo ] bloco ;
params     = ID ":" tipo { "," ID ":" tipo } ;
tipo       = "int" | "bool" | "str" ;

comando    = atribuicao
           | cmd_if
           | cmd_while
           | cmd_print
           | cmd_return
           | bloco ;

atribuicao = ID "=" expr ";" ;
cmd_if     = "if" "(" expr ")" bloco [ "else" bloco ] ;
cmd_while  = "while" "(" expr ")" bloco ;
cmd_print  = "print" expr ";" ;
cmd_return = "return" [ expr ] ";" ;
bloco      = "{" { declaracao } "}" ;

expr       = ou ;
ou         = e { "||" e } ;
e          = igualdade { "&&" igualdade } ;
igualdade  = comparacao { ( "==" | "!=" ) comparacao } ;
comparacao = soma { ( "<" | ">" | "<=" | ">=" ) soma } ;
soma       = produto { ( "+" | "-" ) produto } ;
produto    = unario { ( "*" | "/" | "%" ) unario } ;
unario     = ( "-" | "!" ) unario | chamada ;
chamada    = primario [ "(" [ args ] ")" ] ;
args       = expr { "," expr } ;
primario   = NUM | STR | "true" | "false" | ID | "(" expr ")" ;
```

### Precedência (menor → maior)

```
||  <  &&  <  == !=  <  < > <= >=  <  + -  <  * / %  <  - !  <  chamada  <  primário
```

Todos os binários associam à **esquerda**; unários à **direita**.

---

## 🔤 Especificação léxica

| Token | Padrão (ER) | Exemplos |
|---|---|---|
| `NUM` | `[0-9]+ ( "." [0-9]+ )?` | `42`, `3.14` |
| `STR` | `"([^"\\]\|\\.)*"` | `"oi"`, `"a\"b"` |
| `ID` | `[A-Za-z_][A-Za-z0-9_]*` | `total`, `_x1` |
| Palavras-chave | literais | `let fn if else while print return true false int bool str` |
| Operadores | literais | `+ - * / % == != <= >= < > = && \|\| !` |
| Delimitadores | literais | `( ) { } ; , :` |
| Comentário linha | `"//" [^\n]*` | descartado |
| Comentário bloco | `"/*" ... "*/"` | descartado, **não** aninhado |
| Espaços | `[ \t\r\n]+` | descartado |

⚠️ **Regras obrigatórias do scanner** (Aula 07):
1. **Longest match** — vence o maior lexema
2. **Prioridade por ordem** — palavras-chave declaradas **antes** de `ID`
3. Cada token carrega `linha` e `coluna`

---

## 🧠 Regras semânticas

| # | Regra | Erro se violada |
|---|---|---|
| S1 | Toda variável usada foi **declarada** antes | `variável 'x' não declarada` |
| S2 | Nenhuma variável é **redeclarada** no mesmo escopo | `'x' já declarada neste escopo` |
| S3 | Tipos de operandos são **compatíveis** | `não é possível somar int e bool` |
| S4 | Condição de `if`/`while` é **bool** | `condição deve ser bool, achei int` |
| S5 | Atribuição respeita o **tipo declarado** | `atribuição de bool a variável int` |
| S6 | `return` só dentro de função | `return fora de função` |
| S7 | Tipo do `return` casa com a assinatura | `retorno int em função bool` |
| S8 | Chamada tem a **aridade** correta | `dobro espera 1 argumento, recebeu 2` |
| S9 | Escopos são **aninhados** (blocos criam escopo) | — |

Toda mensagem de erro deve incluir **linha e coluna**.

```
erro semântico em 4:9: variável 'totl' não declarada
    print totl;
          ^^^^
```

---

## ⚙️ Código intermediário (TAC)

Código de três endereços, uma operação por linha:

```
// fonte
let x = 2 * (3 + 4);

// TAC
t0 = 3 + 4
t1 = 2 * t0
x  = t1
```

```
// fonte
while (n > 1) { fat = fat * n; n = n - 1; }

// TAC
L0:
  t0 = n > 1
  ifFalse t0 goto L1
  t1 = fat * n
  fat = t1
  t2 = n - 1
  n = t2
  goto L0
L1:
```

**Instruções obrigatórias:** `=`, binárias (`+ - * / % == != < > <= >= && ||`),
unárias (`- !`), `goto L`, `ifFalse t goto L`, `param t`, `call f, n`, `return t`,
`print t`, `label L`.

---

## 🖥️ Máquina virtual de pilha

| Instrução | Efeito |
|---|---|
| `PUSH k` | empilha constante |
| `LOAD x` | empilha valor da variável |
| `STORE x` | desempilha e grava na variável |
| `ADD SUB MUL DIV MOD` | desempilha 2, empilha resultado |
| `EQ NE LT GT LE GE` | comparações |
| `AND OR NOT NEG` | lógicas e negação |
| `JMP n` | salto absoluto |
| `JZ n` | salta se topo == 0 (desempilha) |
| `CALL n, k` · `RET` | chamada e retorno (nível 3) |
| `PRINT` | desempilha e imprime |
| `HALT` | encerra |

```python
# execução esperada
$ uv run minilang fatorial.ml
3628800

$ uv run minilang fatorial.ml --emit tokens   # lista de tokens
$ uv run minilang fatorial.ml --emit ast      # AST em árvore
$ uv run minilang fatorial.ml --emit tac      # código de 3 endereços
$ uv run minilang fatorial.ml --emit asm      # bytecode da VM
$ uv run minilang fatorial.ml --trace         # traço de execução da VM
```

---

## 📅 Marcos e cronograma

| Marco | Aula | Entrega | Peso no projeto |
|---|---|---|---|
| **M1** | 27 | Scanner: tokens com linha/coluna, longest match, erros léxicos | 15% |
| **M2** | 32 | Parser: AST completa, precedência correta, erros sintáticos com posição | 25% |
| **M3** | 35 | Semântica: tabela de símbolos, escopos aninhados, checagem de tipos (S1–S9) | 20% |
| **M4** | 36 | Gerador de TAC com temporários e rótulos | 15% |
| **M5** | 37 | VM de pilha executando os programas de teste | 15% |
| **M6** | 40 | Apresentação (15 min) + relatório (6–10 pág.) | 10% |

Cada marco é um **PR** com título `[MiniLang M1] Seu Nome`.

---

## 🎚️ Níveis de escopo

Escolha seu nível **na Aula 25** e declare no `README.md` do projeto.

| Nível | Escopo | Nota máxima |
|---|---|---|
| **1 — Núcleo** | `let`, atribuição, `if/else`, `while`, `print`, `int`, `bool`, expressões | 8,0 |
| **2 — Completo** | + `str`, `%`, `&&`/`\|\|` com curto-circuito, comentários de bloco, otimizações locais | 10,0 |
| **3 — Avançado** | + funções com parâmetros e recursão, escopo de função, `return` | 10,0 + bônus |

**Bônus adicionais (+0,5 cada, máx. +2,0):**

- Backend alternativo: gerar **LLVM IR** com `llvmlite` (Aula 39)
- Backend alternativo: gerar **WebAssembly** (`.wat`)
- Otimizações: *constant folding*, *dead code elimination*, propagação de cópias
- Mensagens de erro com **realce de coluna** (`^^^^`) e sugestão ("você quis dizer `total`?")
- REPL interativo
- Formatador de código (`minilang fmt`)

---

## ✅ Critérios de avaliação

| Critério | Pontos |
|---|---|
| **Funcionalidade** — compila e executa os programas de teste | 35 |
| **Corretude das fases** — separação clara, cada fase faz o seu papel | 20 |
| **Tratamento de erros** — mensagens com linha/coluna, sem stack trace vazando | 15 |
| **Testes** — `pytest` verde, cobertura ≥ 90% | 15 |
| **Código e organização** — módulos, type hints, docstrings, README | 10 |
| **Apresentação e relatório** | 5 |

### Suíte de aceitação

O repositório de exercícios traz `projeto/testes/` com programas `.ml` e a saída
esperada. Seu compilador deve passar em **todos** os do seu nível:

```
testes/
├── nivel1/
│   ├── fatorial.ml          + fatorial.out
│   ├── fibonacci.ml         + fibonacci.out
│   ├── primos.ml            + primos.out
│   ├── escopos.ml           + escopos.out
│   └── erros/               programas que DEVEM falhar,
│       ├── nao_declarada.ml   com a mensagem esperada em .err
│       ├── tipo_errado.ml
│       └── falta_ponto_virgula.ml
├── nivel2/
└── nivel3/
```

```bash
uv run pytest projeto/testes/ -v      # roda a suíte de aceitação
```

---

## 📄 Relatório final (6–10 páginas)

Estrutura obrigatória:

1. **Visão geral** — a arquitetura em um diagrama, e por que essas fases
2. **Decisões de projeto** — 3 escolhas técnicas e as alternativas descartadas
3. **A teoria aplicada** — onde cada conceito do Bloco 1–4 apareceu no código
   (cite arquivo e linha: AFD no scanner, GLC no parser, pilha na VM, ...)
4. **O que não funciona** — limitações conhecidas, honestamente descritas
5. **Métricas** — LOC por fase, cobertura de testes, tempo de compilação de um
   arquivo de 1000 linhas
6. **Se eu fizesse de novo** — o que mudaria

> 🎯 A seção 3 é a que amarra o semestre: é onde você mostra que o compilador é a
> **aplicação** da teoria, não um projeto paralelo.

---

## 🏗️ Estrutura sugerida do repositório

```
minilang/
├── __init__.py
├── __main__.py            # CLI
├── tokens.py              # dataclass Token, TipoToken
├── scanner.py             # M1
├── ast_nodes.py           # nós da AST
├── parser.py              # M2
├── simbolos.py            # tabela de símbolos com escopos
├── semantica.py           # M3
├── tac.py                 # M4
├── otimizador.py          # bônus
├── vm.py                  # M5
├── erros.py               # ErroLexico, ErroSintatico, ErroSemantico
└── README.md              # nível escolhido, como rodar, exemplos
tests/
└── test_*.py
```

---

## 🚦 Comece agora (Aula 25)

```bash
uv init minilang && cd minilang
uv python pin 3.13
uv add pytest pytest-cov
# opcionais, conforme o nível/bônus:
uv add ply lark llvmlite

mkdir -p minilang tests
```

O scanner da **Aula 07** já é o ponto de partida do M1 — não jogue fora.

---

**Dúvidas?** Abra uma Issue ou pergunte em sala. Atendimento: segundas, 30 min
antes e após a aula.
