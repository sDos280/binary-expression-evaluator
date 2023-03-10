# The BEE parser
a math binary expression evaluator writen in python


# Parser grammar

expression grammar:
```
expression -> term {-|+ term}
term       -> factor {*|/ term}
factor     -> integer | float | (expression) | -factor | function_name({expression,}) 
```
