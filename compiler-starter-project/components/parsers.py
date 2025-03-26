from components.lexica import MyLexer
from components.memory import Memory
from sly import Parser

class MyParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
        )

    def __init__(self):
        self.memory:Memory = Memory()

    """
    @_('NAME ASSIGN expr')
    def statement(self, p):
        var_name = p.NAME
        value = p.expr
        self.memory.set(var_name, value, type(value))  # Fix: Corrected variable name
        # Note that I did not return anything
        print(f"Stored: {var_name} = {value}")

    @_('expr')
    # S -> E
    def statement(self, p):
        return p.expr

    """
    @_('NAME ASSIGN expr', 'expr')
    def statement(self, p):
        if len(p) == 3:
            var_name = p.NAME
            value = p.expr
            self.memory.set(var_name, value, type(value))
            print(f"Stored: {var_name} = {value}")
        else:
            return p.expr
        

    # The example with literals
    @_('expr PLUS expr')
    # E -> E + E
    def expr(self, p):
        # You can refer to the token 2 ways
        # Way1: using array
        print(p[0], p[1], p[2])
        # Way2: using symbol name. 
        # Here, if you have more than one symbols with the same name
        # You have to indiciate the number at the end.
        return p.expr0 + p.expr1

    # The example with normal token
    @_('expr MINUS expr')
    def expr(self, p):
        print(p[0], p[1], p[2])
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    # https://sly.readthedocs.io/en/latest/sly.html#dealing-with-ambiguous-grammars
    # `%prec UMINUS` is the way to override the `precedence` of MINUS to UMINUS.
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return Expression_number(float(p.NUMBER))


from components.ast.statement import Expression, Expression_math, Expression_number, Operations
class ASTParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', PLUS, MINUS),
        ('left', TIMES, DIVIDE),
        # ('right', UMINUS),
        )

    @_('expr')
    def statement(self, p):
        p.expr.run()
        return p.expr.value

    @_('expr PLUS expr')
    def expr(self, p):
        # parameter1 = p.expr0
        # parameter2 = p.expr1
        return  Expression_math(Operations.PLUS, p.expr0, p.expr1)
       
    
    @_('expr MINUS expr')
    def expr(self, p) -> Expression:
        # parameter1 = p.expr0
        # parameter2 = p.expr1
        return  Expression_math(Operations.MINUS, p.expr0, p.expr1)

    @_('NUMBER')
    def expr(self, p):
        return Expression_number(float(p.NUMBER))
        
        

        
if __name__ == "__main__":
    lexer = MyLexer()
    parser = MyParser()
    test_expression = "9 + 2 * (3 - 1)"
    memory = Memory()
    # parser = ASTParser()
    # text = "1 + 2 + 3"
    result = parser.parse(lexer.tokenize(test_expression))
    print("Result:", result)
    # print(memory)