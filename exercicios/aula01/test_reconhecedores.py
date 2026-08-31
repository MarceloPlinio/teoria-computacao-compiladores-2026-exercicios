from reconhecedores import reconhece_abc, balanceado, palindromo, tokenize


def test_abc():
    # Vazio: n = 0
    assert reconhece_abc("")

    # Caso válido
    assert reconhece_abc("abc")

    # Caso válido maior
    assert reconhece_abc("aaabbbccc")

    # Quantidades diferentes
    assert not reconhece_abc("aabbc")

    # Ordem incorreta
    assert not reconhece_abc("abcabc")


def test_balanceado():
    # Caso vazio
    assert balanceado("")

    # Parênteses
    assert balanceado("()")

    # Aninhamento de diferentes delimitadores
    assert balanceado("([{}])")

    # Outros caracteres devem ser ignorados
    assert balanceado("abc(123)[x]{y}")

    # Delimitadores incompatíveis
    assert not balanceado("(]")

    # Aninhamento incorreto
    assert not balanceado("([)]")

    # Delimitador sem fechamento
    assert not balanceado("(((")


def test_palindromo():
    # Caso vazio
    assert palindromo("")

    # Um único caractere
    assert palindromo("a")

    # Palíndromo de tamanho ímpar
    assert palindromo("aba")

    # Palíndromo de tamanho par
    assert palindromo("abba")

    # Não é palíndromo
    assert not palindromo("aab")

    # Outro caso inválido
    assert not palindromo("abab")


def test_tokenize():
    # Caso básico
    assert tokenize("x = 1;") == [
        ("ID", "x"),
        ("ASSIGN", "="),
        ("NUM", "1"),
        ("SEMI", ";"),
    ]

    # Palavra-chave, identificador, operador e número
    assert tokenize("while (qtd <= 100)") == [
        ("WHILE", "while"),
        ("LPAREN", "("),
        ("ID", "qtd"),
        ("LE", "<="),
        ("NUM", "100"),
        ("RPAREN", ")"),
    ]

    # Longest match: <= deve ser um único token
    assert tokenize("a<=-1")[1] == ("LE", "<=")

    # Número decimal
    assert tokenize("preco = 0.5;") == [
        ("ID", "preco"),
        ("ASSIGN", "="),
        ("NUM", "0.5"),
        ("SEMI", ";"),
    ]

    # Comentários e espaços são ignorados
    assert tokenize("// comentário\nx = 5;") == [
        ("ID", "x"),
        ("ASSIGN", "="),
        ("NUM", "5"),
        ("SEMI", ";"),
    ]

    # Caractere inválido deve gerar ValueError
    try:
        tokenize("x = @;")
        assert False
    except ValueError:
        assert True