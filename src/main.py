import src.bee_tokenizer

if __name__ == '__main__':
    input_string: str = "5 + 6 * 3.656 - 9656"

    tk: src.bee_tokenizer.Tokenizer = src.bee_tokenizer.Tokenizer(input_string)

    tk.tokenize()

    [print(i.string) for i in tk.tokens]

