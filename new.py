from ply import lex
import ply.yacc as yacc
class MyLexer(object):
    
    tokens = (
        'ID',
        'PRINT',
        'PLUS',
        'MINUS',
        'TIMES',
        'DIV',
        'LPAREN',
        'RPAREN',
        'NUMBER',
        'ASSIGN',
    )

    t_ignore = '\t'
    t_ignore_space = '\ '
    t_PLUS    = r'\+'
    t_MINUS   = r'-'
    t_TIMES   = r'\*'
    t_DIV     = r'/'
    t_LPAREN  = r'\('
    t_RPAREN  = r'\)'
    t_PRINT   = r'print'
    t_ASSIGN  = r'='
    t_ID      = r'[a-zA-Z_][a-zA-Z_0-9]*'
 

    def t_NUMBER( self,t ) :
        r'[0-9]+'
        t.value = int( t.value )
        return t

    def t_newline( self,t ):
        r'\n+'
        t.lexer.lineno += len( t.value )

    def t_error(self, t ):
        print("Invalid Token:",t.value[0])
        t.lexer.skip( 1 )

    def t_COMMENT(self,t):
        r'\#.*'
        pass

    # Build the lexer
    def build(self,**kwargs):
         self.lexer = lex.lex(module=self, **kwargs)
     
     # Test it output
    def test(self,data):
         self.lexer.input(data)
         while True:
              tok = self.lexer.token()
              if not tok: 
                  break
              print(tok)
class MyParser(object):
    tokens = MyLexer.tokens
    precedence = (
        ( 'nonassoc', 'PRINT' ),
        ( 'left', 'PLUS', 'MINUS' ),
        ( 'left', 'TIMES', 'DIV' ),
        ( 'nonassoc', 'UMINUS' )
    )

    def p_id_statement(self,p):
        'expr : ID ASSIGN expr'
        p[1] = p[3]
    
    def p_id(self,p):
        'expr : ID'
        p[0] = p[1]
    
    def p_print_statement(self,p):
        'expr : PRINT expr'
        p[0] = p[2]
    
    
    
    def p_empty(self,p):
        'expr : '
        pass

    def p_add( self,p ) :
        'expr : expr PLUS expr'
        p[0] = p[1] + p[3]

    def p_sub( self,p ) :
        'expr : expr MINUS expr'
        p[0] = p[1] - p[3]

    def p_expr2uminus(self, p ) :
        'expr : MINUS expr %prec UMINUS'
        p[0] = - p[2]

    def p_mult_div(self, p ) :
        '''expr : expr TIMES expr
                | expr DIV expr'''

        if p[2] == '*' :
            p[0] = p[1] * p[3]
        else :
            if p[3] == 0 :
                print("Can't divide by 0")
                raise ZeroDivisionError('integer division by 0')
            p[0] = p[1] / p[3]

    def p_expr2NUM( self,p ) :
        'expr : NUMBER'
        p[0] = p[1]

    def p_parens( self,p ) :
        'expr : LPAREN expr RPAREN'
        p[0] = p[2]

    def p_error(self, p ):
        print("Syntax error in input!")

    def build(self,**kwargs):
         self.parser = yacc.yacc(module=self, **kwargs)
   
    def test(self):
        while True:
            text  = input("Roo > ")
            if text == "exit":
                break
            res = self.parser.parse(text)# the input
            if res == None:
                pass
            else:
                print(res)

if __name__ == "__main__":
    l = MyLexer()
    l.build()
    l.test("a = 10")
    p = MyParser()
    p.build()
    p.test()
    