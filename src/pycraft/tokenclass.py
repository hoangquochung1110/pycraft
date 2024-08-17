from enum import Enum

TokenType = Enum(
    "TokenType",
    "LEFT_PAREN, RIGHT_PAREN, LEFT_BRACE, RIGHT_BRACE, \
        COMMA, DOT, MINUS, PLUS, SEMICOLON, SLASH, STAR, \
    BANG, BANG_EQUAL, \
    EQUAL, EQUAL_EQUAL, \
    GREATER, GREATER_EQUAL, \
    LESS, LESS_EQUAL, \
    IDENTIFIER, STRING, NUMBER, \
    AND, CLASS, ELSE, FALSE, FUN, FOR, IF, NIL, OR, \
    PRINT, RETURN, SUPER, THIS, TRUE, VAR, WHILE, \
    EOF\
    "
)


class Token:

    # Adding slots to minimize memory usage since we'll have a lot of tokens
    __slots__ = "type", "lexeme", "literal", "line"

    def __init__(self, typ: TokenType, lexeme: str, literal: object | None, line: int):
        self.type: TokenType = typ
        self.lexeme: str = lexeme
        self.literal: object | None = literal
        self.line: int = line  # TODO: more precise column, line

    def __str__(self) -> str:
        return "{token_type} {literal_or_lexeme}".format(
            token_type=self.type.name,
            literal_or_lexeme=self.literal or self.lexeme,
        )
