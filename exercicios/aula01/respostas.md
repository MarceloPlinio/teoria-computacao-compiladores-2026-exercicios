# Exercício — Aula 01: Introdução à Teoria da Computação e aos Compiladores

## Parte A — Conceitual

### A1

Um sistema gerador é responsável por produzir as palavras que pertencem a uma determinada linguagem seguindo um conjunto de regras. Já um sistema reconhecedor recebe uma palavra pronta e verifica se ela pertence ou não à linguagem.

Como exemplo, podemos considerar a linguagem:

**L = { aⁿbⁿ | n ≥ 0 }**

Essa linguagem possui palavras com a mesma quantidade de `a` e `b`, sendo todos os `a` colocados antes dos `b`. Por exemplo, `""`, `ab`, `aabb` e `aaabbb` pertencem à linguagem, enquanto `aba` e `aab` não pertencem.

Uma gramática que gera essa linguagem pode ser definida por:

```text
S → aSb
S → ε
```

A regra `S → aSb` adiciona um `a` no início e um `b` no final, enquanto a regra `S → ε` encerra a geração.

Por exemplo:

```text
S → aSb
  → aaSbb
  → aaεbb
  → aabb
```

Assim, a gramática funciona como um sistema gerador, pois produz palavras válidas da linguagem.

Um reconhecedor para essa mesma linguagem receberia uma cadeia e verificaria se ela possui todos os `a` antes dos `b` e se a quantidade de `a` é igual à quantidade de `b`.

Esboço:

```text
              ┌─────────────────────┐
Entrada ────→ │ verificar formato   │
              │ a* seguido de b*    │
              └──────────┬──────────┘
                         ↓
              ┌─────────────────────┐
              │ mesma quantidade?   │
              └──────┬────────┬─────┘
                     │ SIM     │ NÃO
                     ↓         ↓
                  ACEITA     REJEITA
```

Por exemplo, ao receber `aabb`, o reconhecedor encontra dois `a` e dois `b` na ordem correta e aceita. Ao receber `aab`, encontra duas ocorrências de `a` e apenas uma de `b`, portanto rejeita.

### A2

| # | Linguagem | Memória mínima | Justificativa |
|---|---|---|---|
| a | Cadeias que começam com `a` | Nenhum além do estado | Basta guardar no estado se o primeiro símbolo lido foi `a` ou não. |
| b | Cadeias com número igual de `a`s e `b`s | Pilha | Uma pilha pode armazenar ocorrências de um símbolo e desempilhá-las ao encontrar ocorrências do outro. |
| c | Cadeias de tamanho múltiplo de 3 | Nenhum além do estado | Basta manter três estados representando o tamanho da cadeia módulo 3. |
| d | Palíndromos | Pilha | É necessário guardar uma quantidade arbitrária de símbolos para compará-los com a segunda metade da cadeia. |
| e | `{ aⁿbⁿcⁿ | n ≥ 1 }` | Memória ilimitada | É necessário comparar três quantidades arbitrárias de símbolos, uma para cada bloco `a`, `b` e `c`. |

### A3

Pipeline de compilação para:

```text
total = preco * 2 + 5;
```

```text
Código-fonte
     │
     ▼
┌─────────────────────┐
│ 1. Análise léxica   │
└──────────┬──────────┘
           │
           ▼
< ID,total >
< ASSIGN,= >
< ID,preco >
< MUL,* >
< NUM,2 >
< PLUS,+ >
< NUM,5 >
< SEMI,; >
           │
           ▼
┌─────────────────────┐
│ 2. Análise sintática│
└──────────┬──────────┘
           │
           ▼
        Atribuição
        /         \
     total          +
                  /   \
              preco    *
                       / \
                      2   5

           │
           ▼
┌──────────────────────┐
│ 3. Análise semântica │
└──────────┬───────────┘
           │
           ▼
Verifica se os identificadores são válidos e se
os tipos envolvidos na operação são compatíveis.

           │
           ▼
┌────────────────────────────┐
│ 4. Representação           │
│    intermediária (IR)      │
└─────────────┬──────────────┘
              │
              ▼
t1 = preco * 2
t2 = t1 + 5
total = t2

              │
              ▼
┌─────────────────────┐
│ 5. Otimização       │
└──────────┬──────────┘
           │
           ▼
A representação intermediária é analisada e
pode ser simplificada ou melhorada sem alterar
o comportamento do programa.

           │
           ▼
┌─────────────────────┐
│ 6. Geração de código│
└──────────┬──────────┘
           │
           ▼
Código de máquina/assembly para a arquitetura alvo.

Exemplo conceitual:

LOAD  preco
MUL   2
ADD   5
STORE total
```

### A4

Sem uma representação intermediária, cada linguagem-fonte precisaria de um tradutor completo para cada arquitetura.

Como são 4 linguagens e 5 arquiteturas:

```text
4 × 5 = 20
```

Portanto, seriam necessários **20 tradutores completos**.

Com uma representação intermediária, cada linguagem precisa de um tradutor para a representação intermediária e cada arquitetura precisa de um tradutor da representação intermediária para seu código de máquina.

Assim:

```text
4 tradutores para gerar a IR
+
5 tradutores da IR para as arquiteturas
=
9 tradutores
```

Portanto, com representação intermediária são necessários **9 tradutores**.

A vantagem é que a representação intermediária separa a parte dependente da linguagem da parte dependente da arquitetura. Isso reduz a quantidade de combinações necessárias e permite reutilizar os componentes.

O LLVM adota essa estratégia porque utiliza uma representação intermediária comum, permitindo que diferentes linguagens possam ser compiladas para ela e que diferentes arquiteturas possam receber código gerado a partir dessa mesma representação.

### A5

| Ferramenta | Classificação | Justificativa |
|---|---|---|
| `gcc` | Compilador | Traduz código-fonte, como C, para código de máquina ou código objeto. |
| `CPython` | Híbrido | O código Python é convertido para bytecode e depois executado pela máquina virtual do CPython. |
| `javac + JVM` | Híbrido | `javac` compila Java para bytecode e a JVM executa esse bytecode, podendo também realizar compilação JIT. |
| `tsc` | Compilador | Transforma TypeScript em JavaScript antes da execução. |
| V8 (JavaScript) | Híbrido | O motor executa JavaScript utilizando técnicas de interpretação e compilação JIT. |
| `rustc` | Compilador | Traduz programas Rust para código de máquina durante a compilação. |

## Parte B — Tokenização manual

### B1

Código original:

```c
// calcula desconto
while (qtd <= 100) {
    preco = preco - 0.5;
    qtd = qtd + 1;
}
```

Os espaços e o comentário são descartados. A tokenização é:

```text
<WHILE, while>
<LPAREN, (>
<ID, qtd>
<LE, <=>
<NUM, 100>
<RPAREN, )>
<LBRACE, {>
<ID, preco>
<ASSIGN, =>
<ID, preco>
<MINUS, ->
<NUM, 0.5>
<SEMI, ;>
<ID, qtd>
<ASSIGN, =>
<ID, qtd>
<PLUS, +>
<NUM, 1>
<SEMI, ;>
<RBRACE, }>
```

### B2

Sem a regra do maior casamento possível (`longest match`), a sequência:

```text
a<=-1
```

poderia ser tokenizada de duas formas.

A tokenização correta, considerando `<=` como um operador de dois caracteres, é:

```text
<ID, a>
<LE, <=>
<MINUS, ->
<NUM, 1>
```

Sem `longest match`, também poderia ocorrer:

```text
<ID, a>
<LT, <>
<ASSIGN, =>
<MINUS, ->
<NUM, 1>
```

O problema é que `<=` deve ser reconhecido como um único operador. A regra do maior casamento possível faz o scanner escolher o token de maior tamanho quando mais de uma regra pode ser aplicada.

### B3

No caso:

```text
x = = 5;
```

o scanner consegue reconhecer os símbolos individualmente, pois `x`, `=`, `=` e `5` são tokens válidos. O problema de dois operadores de atribuição seguidos é uma questão da **análise sintática**, que verifica se a sequência de tokens segue a estrutura esperada pela linguagem.

No caso:

```text
y = z + 1;
```

o scanner também consegue tokenizar a sequência normalmente:

```text
<ID, y>
<ASSIGN, =>
<ID, z>
<PLUS, +>
<NUM, 1>
<SEMI, ;>
```

O fato de `z` nunca ter sido declarado não é um problema léxico. Esse erro é detectado na **análise semântica**, que verifica informações como declaração e uso de identificadores.

Portanto:

```text
x = = 5;       → análise sintática
y = z + 1;     → análise semântica
```

## Parte D — Desafio bônus

### D1

Suponha que exista um programa `H` capaz de reconhecer se qualquer programa Python termina sua execução.

Isso significa que `H(P)` responderia "sim" quando o programa `P` termina e "não" quando `P` entra em execução infinita.

Agora construímos um programa `D` que recebe um programa `P` e faz o contrário da resposta de `H`.

Se `H(P)` disser que `P` termina, então `D` entra em loop infinito.

Se `H(P)` disser que `P` não termina, então `D` termina.

Agora executamos `D` recebendo o próprio `D` como entrada.

Se `H(D)` disser que `D` termina, então, pela definição de `D`, ele deveria entrar em loop, contradizendo a resposta de `H`.

Se `H(D)` disser que `D` não termina, então `D` deveria terminar, contradizendo novamente a resposta de `H`.

Nos dois casos existe uma contradição. Portanto, não pode existir um programa que reconheça corretamente, para qualquer programa Python, se sua execução termina.