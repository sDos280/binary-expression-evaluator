import src.bee_tokenizer
import src.bee_parser

if __name__ == '__main__':
    input_string: str = "sin(5 + 6) * 3.656 - 9656 * -652 / 5"

    tk: src.bee_tokenizer.Tokenizer = src.bee_tokenizer.Tokenizer(input_string)



    tk.tokenize()

    pr: src.bee_parser.Parser = src.bee_parser.Parser(tk.tokens)


    print(pr.start_node)
    print("The expression is evaluated to:", pr.start_node.eval())



