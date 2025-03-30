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
        self.memory.set(variable_name=var_name,value=value, data_type=type(value))
        # Note that I did not return anything

    @_('expr')
    def statement(self, p) -> int:
        return p.expr

    # The example with literals
    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    # The example with normal token
    @_('expr MINUS expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr TIMES expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr DIVIDE expr')
    def expr(self, p):
        return p.expr0 / p.expr1

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return int(p.NUMBER)
    
    def pre_fix_expr(self, input_text):
        tokens = input_text.split()
        prefix = []
        operator_stack = []
        precedence = {'+': 2, '-': 2, '*': 1, '/': 1}

        for token in reversed(list(tokens)):
            if token.isdigit():
                prefix.append(token)
            elif token in precedence:
                while (operator_stack and
                    precedence[token] <= precedence[operator_stack[-1]]):
                    prefix.append(operator_stack.pop())
                operator_stack.append(token)

        while operator_stack:
            prefix.append(operator_stack.pop())
        prefix.reverse()
        prefix_str = ' '.join(prefix)

        return prefix_str
    
    def post_fix_expr(self, expression):
        operator_stack = []
        postfix = []
        tokens = expression.split()
        precedence = {'+': 2, '-': 2, '*': 1, '/': 1}

        for token in tokens:
            if token.isdigit():
                postfix.append(token)
            else:
                while operator_stack and precedence.get(operator_stack[-1], 0) >= precedence.get(token, 0):
                    postfix.append(operator_stack.pop())
                operator_stack.append(token)
        
        postfix.extend(reversed(operator_stack))
        postfix_str = ' '.join(postfix)

        return postfix_str
    
    # def convert_to_infix(self, expression):
    #     """ Convert prefix notation to infix manually """
        
    #     tokens = expression.strip().split()

    #     # ✅ Ensure the prefix expression starts with an operator
    #     if not tokens[0] in {'+', '-', '*', '/'}:
    #         raise ValueError(f"❌ Prefix expression must start with an operator: {expression}")

    #     # Reverse the token list for processing
    #     tokens.reverse()
    #     stack = []

    #     print(f" Tokens (Reversed): {tokens}")    # Debugging

    #     for token in tokens:
    #         if token.isdigit():                     # If it's a number, push it onto the stack
    #             stack.append(token)
    #         # elif token.lstrip('-').isdigit():       # Handle negative numbers
    #         #     stack.append(token)
    #         elif token in {'+', '-', '*', '/'}:     # If operator, pop two operands and construct expression
    #             if len(stack) < 2:
    #                 print(f"❌ Operator '{token}' is missing operands. Stack before error: {stack}")
    #                 raise ValueError(f"❌ Invalid prefix expression: {expression} (Operator '{token}' has fewer than 2 operands)")

    #             op1 = stack.pop()
    #             op2 = stack.pop()
    #             new_expr = f"({op1} {token} {op2})"  # Construct infix expression
    #             stack.append(new_expr)

    #             print(f"🔹 Processed Operator '{token}': {new_expr}")  # Debugging
    #         else:
    #             raise ValueError(f"❌ Invalid character in expression: {token}")

    #     if len(stack) != 1:
    #         raise ValueError(f"❌ Invalid prefix expression: {expression} (Stack leftover: {stack})")

    #     return stack[0]  # The final infix expression

    # def convert_to_infix(self, expression):
    #     tokens = expression.strip().split()
    #     stack = []
    #     operators = {'+', '-', '*', '/'}

    #     for token in reversed(tokens):
    #         if token.isdigit():
    #             stack.append(token)
    #         elif token in operators:
    #             if len(stack) < 2:
    #                 raise ValueError(f"Invalid expression: {expression}")
    #             op1 = stack.pop()
    #             op2 = stack.pop()
    #             stack.append(f"({op1} {token} {op2})")
    #         else:
    #             raise ValueError(f"Unexpected token: {token}")

    #     if len(stack) != 1:
    #         raise ValueError(f"Malformed expression: {expression}")

    #     return stack[0]

    def convert_to_infix(self, expression):
        """ Convert prefix notation to infix and evaluate it """
        
        tokens = expression.strip().split()

        # Ensure valid prefix notation
        if not tokens[0] in {'+', '-', '*', '/'}:
            raise ValueError(f"❌ Prefix expression must start with an operator: {expression}")

        tokens.reverse()  # Reverse for processing
        stack = []

        for token in tokens:
            if token.isdigit():  
                stack.append(token)
            elif token in {'+', '-', '*', '/'}:
                if len(stack) < 2:
                    raise ValueError(f"❌ Invalid prefix expression: {expression}")

                op1 = stack.pop()
                op2 = stack.pop()
                new_expr = f"({op1} {token} {op2})"
                stack.append(new_expr)
            else:
                raise ValueError(f"❌ Invalid token: {token}")

        if len(stack) != 1:
            raise ValueError(f"❌ Invalid expression: {expression}")

        infix_expr = stack[0]

        # ✅ Evaluate the infix expression safely
        try:
            result = eval(infix_expr, {"__builtins__": None}, {})
        except Exception as e:
            raise ValueError(f"Evaluation Error: {e}")

        return infix_expr, result  # Return both infix string and computed result