
import sly
Comentarios=[]
class Lexer(sly.Lexer):
    tokens = {
        # Palabras Reservadas
        BREAK, CHAR, CONST, CONTINUE, ELSE, EXTERN, FLOAT,
        FOR, IF, INT, RETURN, STATIC, VOID, WHILE,

        # Operadores
        LE, GE, EQ, NE, LAND, LOR,LT,GT,
        ADDEQ, SUBEQ, MULEQ,DIVEQ,MODEQ,

        # Tokens complejos
        ID, INUMBER, FNUMBER, CHARACTER, STRING, ELLIPSIS,
    }
    literals = '+-*/%=<>!&(){}[]:;,.'

    # Ignorar espacios en blanco (white-spaces)
    ignore = ' \t\r'

    # Operadores de relacion
    LE = r'<='
    GE = r'>='
    EQ = r'=='
    NE = r'!='
    LT = r'<'
    GT = r'>'
    # Operadores logicos
    LOR  = r'\|\|'
    LAND = r'&&'

    ADDEQ = r'\+='
    SUBEQ = r'-='
    MULEQ = r'\*='
    DIVEQ = r'/='
    MODEQ = r'%='

    # Identificador
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'

    # Casos Especiales (Palabras Reservadas)
    ID['break']    = BREAK 
    ID['char']     = CHAR 
    ID['const']    = CONST 
    ID['continue'] = CONTINUE 
    ID['else']     = ELSE 
    ID['extern']   = EXTERN 
    ID['float']    = FLOAT 
    ID['for']      = FOR 
    ID['if']       = IF
    ID['int']      = INT
    ID['return']   = RETURN 
    ID['static']   = STATIC 
    ID['void']     = VOID
    ID['while']    = WHILE
    
   
   

    ELLIPSIS = r'\.\.\.'
    
    # literals
    CHARACTER = r"'\w'"
    @_(r'\'.\'')
    def CHARACTER(self, t):
        return t
    
    @_(r'[0-9]*\.[0-9]+e?[\+|\-]?[0-9]*')
    def FNUMBER(self, t):
        t.value = float(t.value)
        return t
    
    STRING = r'\"(.)*?\"'
    
    
    @_(r'\"(.|\\n|\\t|\\)*\\[a-mo-su-zA-MO-SU-Z0-9_](.|\\n|\\t|\\)*\"')
    def error_esc(self,t):
        
        b = self.lineno
        a ="Cadena con codigo de escape no permitido ln "+ str(b)
        Comentarios.append(a)
        self.index += 1

    @_(r'\"(.|\n)*')
    def error_str(self, t):
        
        b = self.lineno
        a ="Cadena incompleta en la ln "+ str(b)
        Comentarios.append(a)
        self.index += 1

    @_(r'\"(.)*?\"')
    def STRING_LIT(self, t):
        return t

  
    
    @_(r'\/\*([^*]|\*[^\/])*\*\/')
    def ignore_bloccomment(self, t):
        self.lineno += t.value.count('\n')
        b = self.lineno
        a ="Bloque de comentarios con fin en la linea "+ str(b)
        Comentarios.append(a)
        
    
    @_(r'(/\*(.|\n)*\*/)|(//.*)')
    def ignore_linecomment(self, t):
        self.lineno += t.value.count('\n')
        b = self.lineno
        a ="Comentario de una linea, ln "+ str(b)
        Comentarios.append(a)
       
        
    @_(r'/\*(.|\n)*')
    def ignore_commentoclosed(self, t):
        
        b = self.lineno
        a ="Comentario no cerrado en ln"+ str(b)
        Comentarios.append(a)

    # Ignorar newline
    @_('\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"[red]{self.lineno}: Caracter '{t.value[0]}' es ilegal[/red]")
        self.index += 1

    @_(r'0?[x|b|o]?[0-9]+', r'\d+')
    def INUMBER(self, t):
        if t.value.startswith('0x'):
            t.value = int(t.value[2:], 16)
        elif t.value.startswith('0o'):
            t.value = int(t.value[2:], 8)
        elif t.value.startswith('0b'):
            t.value = int(t.value[2:], 2)
        else:
            t.value = int(t.value)
        return t

def pprint(source):
    from rich.table   import Table
    from rich.console import Console
    

    lex = Lexer()
    print(" \n Comentarios : \n")
    

    table = Table(title='Analizador Léxico')
    table.add_column('token')
    table.add_column('value')
    table.add_column('lineno', justify='right')

   
    for tok in lex.tokenize(source):
        value = tok.value if isinstance(tok.value, str) else str(tok.value)
        table.add_row(tok.type, value, str(tok.lineno))
    
    console = Console()
    for comentario in Comentarios:
            print(comentario)

    print("\n")
    console.print(table, justify='center')
    
    
            

if __name__ == '__main__':
    import sys

    if len(sys.argv) != 2:
       sys.stderr.write(f"usage: python {sys.argv[0]} fname")
       raise SystemExit(1)

    pprint(open(sys.argv[1], encoding='utf-8').read())