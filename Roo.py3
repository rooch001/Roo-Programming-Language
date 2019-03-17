from sly import Lexer
from sly import Parser

class Lex(Lexer):
    tokens = { 
        NAME, 
        NUMBER, 
        STRING, 
        WHENEVER, 
        OTHERWISE, 
        FROM, 
        SUBROUTINE, 
        TO, 
        EQEQ,
        LPAREN,
        RPAREN ,
        LSPAREN,
        RSPAREN,
        PRINT

        }

    ignore = '\t '
    ignore_comment = r'\#.*'
    ignore_newline = r'\n+'

    literals = { '=', '+', '-', '/', '*', '(', ')', ',', ';','{','}' }

    # Define tokens

    WHENEVER = r'whenever'
    OTHERWISE = r'otherwise'
    FROM = r'from'
    SUBROUTINE = r'subroutine'
    TO = r'to'
    NAME = r'[a-zA-Z_][a-zA-Z0-9_]*'
    STRING = r'\".*?\"'
    LPAREN = r'{'
    RPAREN = r'}'
    EQEQ = r'=='
    PRINT = r'print'
    LSPAREN = r'\('
    RSPAREN = r'\)'
    
    def test(self,text):
        for tok in lexer.tokenize(text):
            print(tok)


    @_(r'\d+')
    def NUMBER(self, t):
        t.value = int(t.value)
        return t

    @_(r'\n+')
    def ignore_newline(self,t):
        self.lineno += t.value.count('\n')  
    
    @_(r'#.*')
    def COMMENT(self, t):
        pass
    
    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1

class Parse(Parser):
    tokens = Lex.tokens

    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/'),
        ('right', 'UMINUS'),
        )

    def __init__(self):
        self.env = { }

    @_('')
    def statement(self, p):
        pass

    @_('PRINT expr')
    def statement(self, p):
        ...

    @_('FROM var_assign TO expr LPAREN\n statement \n RPAREN ";"')
    def statement(self, p):
        return ('for_loop', ('for_loop_setup', p.var_assign, p.expr), p.statement)

    @_('WHENEVER condition LPAREN\n statement \n RPAREN OTHERWISE LPAREN\n statement \n RPAREN ";"')
    def statement(self, p):
        return ('if_stmt', p.condition, ('branch', p.statement0, p.statement1))

    @_('SUBROUTINE NAME LSPAREN RSPAREN LPAREN\n statement \n RPAREN ";"')
    def statement(self, p):
        return ('fun_def', p.NAME, p.statement)

    @_('NAME LSPAREN RSPAREN ";"')
    def statement(self, p):
        return ('fun_call', p.NAME)
    
    @_('expr EQEQ expr')
    def condition(self, p):
        return ('condition_eqeq', p.expr0, p.expr1)

    @_('var_assign')
    def statement(self, p):
        return p.var_assign

    @_('NAME "=" expr')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.expr)

    @_('NAME "=" STRING')
    def var_assign(self, p):
        return ('var_assign', p.NAME, p.STRING)


    @_('expr')
    def statement(self, p):
        return (p.expr)
    


    @_('expr "+" expr')
    def expr(self, p):
        return ('add', p.expr0, p.expr1)

    @_('expr "-" expr')
    def expr(self, p):
        return ('sub', p.expr0, p.expr1)

    @_('expr "*" expr')
    def expr(self, p):
        return ('mul', p.expr0, p.expr1)

    @_('expr "/" expr')
    def expr(self, p):
        return ('div', p.expr0, p.expr1)

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return p.expr
    
    @_("LSPAREN expr RSPAREN")
    def expr(self,p):
        return (p.expr)

    @_('NAME')
    def expr(self, p):
        return ('var', p.NAME)

    @_('NUMBER')
    def expr(self, p):
        return ('num', p.NUMBER)



class Execute:

    def __init__(self, tree, env):
        self.env = env
        result = self.walkTree(tree)
        if result is not None and isinstance(result, int):
            print(result)
        if isinstance(result, str) and result[0] == '"':
            print(result)

    def walkTree(self, node):

        if isinstance(node, int):
            return node
        if isinstance(node, str):
            return node

        if node is None:
            return None

        if node[0] == 'program':
            if node[1] == None:
                self.walkTree(node[2])
            else:
                self.walkTree(node[1])
                self.walkTree(node[2])

        if node[0] == 'num':
            return node[1]
        
        if node[0] == 'str':
            return node[1]

        if node[0] == 'if_stmt':
            result = self.walkTree(node[1])
            if result:
                return self.walkTree(node[2][1])
            return self.walkTree(node[2][2])
        

        if node[0] == 'condition_eqeq':
            return self.walkTree(node[1]) == self.walkTree(node[2])

        if node[0] == 'fun_def':
            self.env[node[1]] = node[2]

        if node[0] == 'fun_call':
            try:
                return self.walkTree(self.env[node[1]])
            except LookupError:
                print("Undefined function '%s'" % node[1])
                return 0

        if node[0] == 'add':
            return self.walkTree(node[1]) + self.walkTree(node[2])
        elif node[0] == 'sub':
            return self.walkTree(node[1]) - self.walkTree(node[2])
        elif node[0] == 'mul':
            return self.walkTree(node[1]) * self.walkTree(node[2])
        elif node[0] == 'div':
            return self.walkTree(node[1]) / self.walkTree(node[2])

        if node[0] == 'var_assign':
            self.env[node[1]] = self.walkTree(node[2])
            return node[1]

        if node[0] == 'var':
            try:
                return self.env[node[1]]
            except LookupError:
                print("Undefined variable '"+node[1]+"' found!")
                return 

        if node[0] == 'for_loop':
            if node[1][0] == 'for_loop_setup':
                loop_setup = self.walkTree(node[1])

                loop_count = self.env[loop_setup[0]]
                loop_limit = loop_setup[1]

                for i in range(loop_count+1, loop_limit+1):
                    res = self.walkTree(node[2])
                    if res is not None:
                        print(res)
                    self.env[loop_setup[0]] = i
                del self.env[loop_setup[0]]

        if node[0] == 'for_loop_setup':
            return (self.walkTree(node[1]), self.walkTree(node[2]))


if __name__ == '__main__':
    lexer = Lex()
    # lexer.test("print 1")
    parser = Parse()
    env = {}
    while True:
        try:
            text = input('Roo > ')
        except EOFError:
            pass
        if text == "PARSER OUTPUT ROO.SHOW();":
            show = open("parser.out","r")
            ans = show.readlines()
            ans = ans[1:]
            for i in ans:
                print(i,end='')
            
        elif text == "exit":
            break
        elif text:
            tree = parser.parse(lexer.tokenize(text))
            Execute(tree, env)