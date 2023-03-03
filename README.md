Here's a corrected version of the writing:

Binary Expression Evaluator
This is a small, easy-to-read binary expression evaluator written in Python. The main goals of our binary expression evaluator are:

To take a string of binary expression and evaluate it.
To be able to understand the "Order of Operations."
So, how do we start implementing that? Let's look at the kind of input we expect: 6 + 5 * 30. If we plug that into a calculator, we get 156. How was the calculator able to compute that?

Tokens
When we see an expression like 6 + 5 * 30, we need a way to represent the string to the computer. To do that, we use the concept of tokens.

Tokens can be thought of as the breaking down of a string into its most valuable data. For example, we know that the expressions 6 + 5 * 30 and 6+5*30 will have the same "interpretation" because we know that white spaces don't really have a real value in the expression string.

So, what actually is the useful data in an expression? The literals and operations, of course. While removing the white spaces of an expression won't affect it, removing any literals or operations can dramatically change the value of an expression. For example, removing the 6 + from 6 + 5 * 30 will dramatically change the value of the expression.

Then, how can we write a tool (tokenizer) that is able to translate a string to its corresponding tokens?

Token Type Declaration:

```python
class Token:
    def __init__(self, kind: TokenKind, string: str) -> None:
        self.kind: TokenKind = kind
        self.string: str = string
```

we declare a `Token` object that contains two fields:

* "string": the string of the token, for example: `6`, `+`, `-362`, `*`, etc.
* "kind": the kind of the token. For example, the token can be `Literal`, like numbers, or an operation symbol, like `Plus`, `Minus`, `Asterisk`, etc.

Tokenizer Class Declaration:

```python
class Tokenizer:
    def __init__(self, input_string: str) -> None:
        self.input_string: str = input_string
        self.tokens: list[Token] = []
```

As you can see here, we declare a Tokenizer object that contains two fields:

* "input_string": The input string to tokenize.
* "tokens": The list of tokens generated from the input string.