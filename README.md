# The BEE parser

a math binary expression evaluator writen in python

# Parser grammar

expression grammar:

```yacc
unary_operator
	: '+'
	| '-'
	;
	
expression_list
	: expression
	| expression_list ',' expression
	;
```

```yacc
primary_expression
	: IDENTIFIER
	| CONSTANT
	| STRING_LITERAL
	| '(' expression ')'
	;
	
postfix_expression
	: primary_expression
	| postfix_expression '(' ')'
	| postfix_expression '(' expression_list ')'
	;
	
unary_expression
	: postfix_expression
	| unary_operator postfix_expression
	;
	
multiplicative_expression
	: unary_expression
	| multiplicative_expression '*' unary_expression
	| multiplicative_expression '/' unary_expression
	| multiplicative_expression '%' unary_expression
	;

additive_expression
	: multiplicative_expression
	| additive_expression '+' multiplicative_expression
	| additive_expression '-' multiplicative_expression
	;

expression
	: additive_expression
	;
```
