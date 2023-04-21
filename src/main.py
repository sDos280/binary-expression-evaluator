import src.bee_lexer
import src.bee_parser

if __name__ == '__main__':
    """input_string: str = "6 + 3 - 8.236 / cos(5 + 6 * 3.2101)"""
    input_string: str = "5 / 8 * 6"

    lexer: src.bee_lexer.Lexer = src.bee_lexer.Lexer(input_string)

    lexer.lex()

    parser: src.bee_parser.Parser = src.bee_parser.Parser(lexer.tokens)

    parser.parse()
