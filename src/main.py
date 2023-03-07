import src.bee_tokenizer
import src.bee_parser

if __name__ == '__main__':
    input_string: str = "5 + 6 * 3.656 - 9656"

    tk: src.bee_tokenizer.Tokenizer = src.bee_tokenizer.Tokenizer(input_string)

    tk.tokenize()

    pr: src.bee_parser.Parser = src.bee_parser.Parser(tk.tokens)

    print(pr.start_node)



