def reconhece_abc(cadeia: str) -> bool:
    """
    Verifica se a cadeia pertence à linguagem { aⁿbⁿcⁿ | n ≥ 0 }.

    Args:
        cadeia: Cadeia formada por símbolos.

    Returns:
        True se a cadeia possui a mesma quantidade de a, b e c,
        nessa ordem; caso contrário, False.
    """
    quantidade_a = cadeia.count("a")
    quantidade_b = cadeia.count("b")
    quantidade_c = cadeia.count("c")

    if quantidade_a != quantidade_b or quantidade_b != quantidade_c:
        return False

    esperada = "a" * quantidade_a + "b" * quantidade_b + "c" * quantidade_c

    return cadeia == esperada

def balanceado(cadeia: str) -> bool:
    """
    Verifica se os parênteses, colchetes e chaves estão corretamente
    balanceados e aninhados.

    Args:
        cadeia: Cadeia que pode conter (), [] e {}.

    Returns:
        True se os delimitadores estiverem corretamente balanceados;
        caso contrário, False.
    """
    pilha = []

    pares = {
        ")": "(",
        "]": "[",
        "}": "{",
    }

    for caractere in cadeia:
        if caractere in "([{":
            pilha.append(caractere)

        elif caractere in ")]}":
            if not pilha or pilha[-1] != pares[caractere]:
                return False

            pilha.pop()

    return len(pilha) == 0

def palindromo(cadeia: str) -> bool:
    """
    Verifica se uma cadeia sobre {a, b} é um palíndromo.

    Args:
        cadeia: Cadeia formada pelos símbolos a e b.

    Returns:
        True se a cadeia for um palíndromo; caso contrário, False.
    """
    esquerda = 0
    direita = len(cadeia) - 1

    while esquerda < direita:
        if cadeia[esquerda] != cadeia[direita]:
            return False

        esquerda += 1
        direita -= 1

    return True

def tokenize(codigo: str) -> list[tuple[str, str]]:
    """
    Converte um código-fonte em uma lista de tokens.

    Args:
        codigo: Código-fonte a ser tokenizado.

    Returns:
        Lista de tuplas contendo o tipo e o lexema de cada token.

    Raises:
        ValueError: Se for encontrado um caractere inválido.
    """
    tokens = []
    i = 0

    palavras_chave = {
        "while": "WHILE",
    }

    operadores_duplos = {
        "<=": "LE",
        ">=": "GE",
        "==": "EQ",
        "!=": "NE",
    }

    operadores_simples = {
        "=": "ASSIGN",
        "<": "LT",
        ">": "GT",
        "+": "PLUS",
        "-": "MINUS",
        "*": "MUL",
        "/": "DIV",
    }

    delimitadores = {
        "(": "LPAREN",
        ")": "RPAREN",
        "{": "LBRACE",
        "}": "RBRACE",
        "[": "LBRACKET",
        "]": "RBRACKET",
        ";": "SEMI",
        ",": "COMMA",
    }

    while i < len(codigo):
        caractere = codigo[i]

        if caractere.isspace():
            i += 1
            continue

        if codigo.startswith("//", i):
            i += 2

            while i < len(codigo) and codigo[i] != "\n":
                i += 1

            continue

        if caractere.isalpha() or caractere == "_":
            inicio = i
            i += 1

            while i < len(codigo) and (
                codigo[i].isalnum() or codigo[i] == "_"
            ):
                i += 1

            lexema = codigo[inicio:i]
            tipo = palavras_chave.get(lexema, "ID")

            tokens.append((tipo, lexema))
            continue

        if caractere.isdigit():
            inicio = i
            i += 1

            while i < len(codigo) and codigo[i].isdigit():
                i += 1

            if i < len(codigo) and codigo[i] == ".":
                i += 1

                if i >= len(codigo) or not codigo[i].isdigit():
                    raise ValueError("Número inválido")

                while i < len(codigo) and codigo[i].isdigit():
                    i += 1

            lexema = codigo[inicio:i]
            tokens.append(("NUM", lexema))
            continue

        operador_duplo = codigo[i:i + 2]

        if operador_duplo in operadores_duplos:
            tokens.append(
                (operadores_duplos[operador_duplo], operador_duplo)
            )
            i += 2
            continue

        if caractere in operadores_simples:
            tokens.append(
                (operadores_simples[caractere], caractere)
            )
            i += 1
            continue

        if caractere in delimitadores:
            tokens.append(
                (delimitadores[caractere], caractere)
            )
            i += 1
            continue

        raise ValueError(f"Caractere inválido: {caractere!r}")

    return tokens