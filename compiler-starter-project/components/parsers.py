from components.lexica import MyLexer
from components.memory import Memory
from sly import Parser
from components.ast.statement import Expression, Expression_math, Expression_number, Operations

class MyParser(Parser):
    debugfile = 'parser.out'
    start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', "+", 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    def __init__(self):
        self.memory:Memory = Memory()

    
    @_('NAME ASSIGN expr')
    def statement(self, p):
        var_name = p.NAME
        value = p.expr
        self.memory.set(variable_name=var_name,value=value, data_type=type(value))  # Fix: Corrected variable name
        # Note that I did not return anything
        # print(f"Stored: {var_name} = {value}")

    @_('expr')
    # S -> E
    def statement(self, p):
        return p.expr


    # The example with literals
    @_('expr "+" expr')
    # E -> E + E
    def expr(self, p):
        # You can refer to the token 2 ways
        # Way1: using array
        print(p[0], p[1], p[2])
        # Way2: using symbol name. 
        # Here, if you have more than one symbols with the same name
        # You have to indiciate the number at the end.
        return p.expr0 + p.expr1

    # @_('NAME ASSIGN expr')
    # def statement(self, p):
    #     self.memory.set(p.NAME, p.expr, type(p.expr))
    #     print(f"Stored: {p.NAME} = {p.expr}")
    #     return p.expr

    # @_('expr')
    # def statement(self, p):
    #     return p.expr
        

    

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
        return int(p.NUMBER)
    

    def convert_to_infix(self, expression):
        """ Convert prefix notation to infix manually """
        stack = []
        tokens = expression.strip().split()

        # ✅ Ensure the prefix expression starts with an operator
        if not tokens[0] in {'+', '-', '*', '/'}:
            raise ValueError(f"❌ Prefix expression must start with an operator: {expression}")

        # Reverse the token list for processing
        tokens.reverse()

        print(f" Tokens (Reversed): {tokens}")    # Debugging

        for token in tokens:
            if token.isdigit():                     # If it's a number, push it onto the stack
                stack.append(token)
            # elif token.lstrip('-').isdigit():       # Handle negative numbers
            #     stack.append(token)
            elif token in {'+', '-', '*', '/'}:     # If operator, pop two operands and construct expression
                if len(stack) < 2:
                    print(f"❌ Operator '{token}' is missing operands. Stack before error: {stack}")
                    raise ValueError(f"❌ Invalid prefix expression: {expression} (Operator '{token}' has fewer than 2 operands)")

                op1 = stack.pop()
                op2 = stack.pop()
                new_expr = f"({op1} {token} {op2})"  # Construct infix expression
                stack.append(new_expr)

                print(f"🔹 Processed Operator '{token}': {new_expr}")  # Debugging
            else:
                raise ValueError(f"❌ Invalid character in expression: {token}")

        if len(stack) != 1:
            raise ValueError(f"❌ Invalid prefix expression: {expression} (Stack leftover: {stack})")

        return stack[0]  # The final infix expression

        # for token in reversed(tokens):
        #     if token.type == "NUMBER":
        #         stack.append(str(token.value))
        #     elif token.type in {"PLUS", "MINUS", "TIMES", "DIVIDE"}:
        #         if len(stack) < 2:
        #             return "Invalid Expression"
        #         op1 = stack.pop()
        #         op2 = stack.pop()
        #         stack.append(f"({op1} {token.value} {op2})")
        #     else:
        #         return "Invalid Expression"
        # return stack[0] if stack else "Invalid Expression"

# ===========================
# 🔹 PREFIX NOTATION PARSER
# ===========================
# class PrefixParser(Parser):
#     debugfile = 'parser.out'            # Debug file
#     start = 'statement'
#     tokens = MyLexer.tokens
#     precedence = (
#         ('left', 'PLUS', 'MINUS'),
#         ('left', 'TIMES', 'DIVIDE'),
#         # ('right', 'UMINUS'),
#     )

#     def __init__(self):
#         self.memory = Memory()
#         # self.infix_stack = []

#     @_('NAME ASSIGN expr')
#     def statement(self, p):
#         self.memory.set(p.NAME, p.expr, type(p.expr))
#         print(f"Stored: {p.NAME} = {p.expr}")
#         return p.expr

#     @_('expr')
#     def statement(self, p):
#         return p.expr

#     def convert_to_infix(self, tokens):
#         """ Convert prefix notation to infix manually """
#         stack = []
#         for token in reversed(tokens):
#             if token.type == "NUMBER":
#                 stack.append(str(token.value))
#             elif token.type in {"PLUS", "MINUS", "TIMES", "DIVIDE"}:
#                 if len(stack) < 2:
#                     return "Invalid Expression"
#                 op1 = stack.pop()
#                 op2 = stack.pop()
#                 stack.append(f"({op1} {token.value} {op2})")
#             else:
#                 return "Invalid Expression"
#         return stack[0] if stack else "Invalid Expression"

#     def get_infix(self):
#         return self.infix_stack[0] if self.infix_stack else ""


#     @_('PLUS expr expr')
#     def expr(self, p):
#         result = p.expr0 + p.expr1
#         right = self.infix_stack.pop()
#         left = self.infix_stack.pop()
#         self.infix_stack.append(f"({left} + {right})")
#         return result

#     @_('MINUS expr expr')
#     def expr(self, p):
#         result = p.expr0 - p.expr1
#         right = self.infix_stack.pop()
#         left = self.infix_stack.pop()
#         self.infix_stack.append(f"({left} - {right})")
#         return result

#     @_('TIMES expr expr')
#     def expr(self, p):
#         result = p.expr0 * p.expr1
#         right = self.infix_stack.pop()
#         left = self.infix_stack.pop()
#         self.infix_stack.append(f"({left} * {right})")
#         return result

#     @_('DIVIDE expr expr')
#     def expr(self, p):
#         if p.expr1 == 0:
#             raise ValueError("Division by zero error")
#         result = p.expr0 / p.expr1
#         right = self.infix_stack.pop()
#         left = self.infix_stack.pop()
#         self.infix_stack.append(f"({left} / {right})")
#         return result

#     @_('NUMBER')
#     def expr(self, p):
#         num = float(p.NUMBER)
#         self.infix_stack.append(str(num))
#         return num

#     def parse(self, tokens):
#         self.infix_stack = []
#         return super().parse(tokens)

    
    


from components.ast.statement import Expression, Expression_math, Expression_number, Operations
class ASTParser(Parser):
    # debugfile = 'parser.out'
    # start = 'statement'
    # Get the token list from the lexer (required)
    tokens = MyLexer.tokens
    precedence = (
        ('left', "+", 'MINUS'),
        ('left', 'TIMES', 'DIVIDE'),
        ('right', 'UMINUS'),
    )

    @_('expr')
    def statement(self, p):
        return p.expr

    @_('expr "+" expr')
    def expr(self, p):
        # parameter1 = p.expr0
        # parameter2 = p.expr1
        return  Expression_math(Operations.PLUS, p.expr0, p.expr1)
       
    
    @_('expr MINUS expr')
    def expr(self, p) -> Expression:
        # parameter1 = p.expr0
        # parameter2 = p.expr1
        return  Expression_math(Operations.MINUS, p.expr0, p.expr1)
    
    @_('expr TIMES expr')
    def expr(self, p):
        return Expression_math(Operations.TIMES, p.expr0, p.expr1)

    @_('expr DIVIDE expr')
    def expr(self, p):
        return Expression_math(Operations.DIVIDE, p.expr0, p.expr1)
    
    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return Expression_math(Operations.MINUS, Expression_number(0), p.expr)

    @_('NUMBER')
    def expr(self, p):
        return Expression_number(float(p.NUMBER))
        
        

        
if __name__ == "__main__":
    lexer = MyLexer()
    parser = MyParser()
    test_expression = "9 + 2 * (3 - 1)"
    
    tokens = list(lexer.tokenize(test_expression))
    result = parser.parse(tokens)

    if isinstance(result, Expression_number):
        print("Result:", result.run())  # Ensure `run()` is valid before calling it
    else:
        print("Parsed AST:", result)
    # print(memory)