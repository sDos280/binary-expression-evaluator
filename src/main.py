import src.bee_tokenizer
import src.bee_parser

if __name__ == '__main__':
    input_string: str = "(5 + 6) * 3.656 - 9656 * -652 / 5"

    tk: src.bee_tokenizer.Tokenizer = src.bee_tokenizer.Tokenizer(input_string)

    tk.tokenize()

    [print(i.string, f": {index}") for index, i in enumerate(tk.tokens)]

    pr: src.bee_parser.Parser = src.bee_parser.Parser(tk.tokens)

    print(pr.start_node)



