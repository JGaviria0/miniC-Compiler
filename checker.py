# checker.py
#
# Este archivo tendrá la parte de verificación/validación de tipo de datos del compilador.  
# Hay una serie de cosas que deben gestionarse para que esto funcione.  Primero, debe 
# tener alguna noción de "tipo" en su compilador.
#
# En segundo lugar, debe administrar entornos/ámbito para manejar los nombres de las 
# definiciones (variables, funciones, etc.).
#
# Una clave para esta parte del proyecto serán las pruebas adecuadas.  
# A medida que agrega código, piense en cómo podría probarlo.
#
# ---------------------------------------------------------------------
# Revisa diferentes aspectos del codigo:
#
# 1. Todos los IDENT deben de estar debidamente declarados, en su
#    respectivo contexto (env)        update: Listo
#
# 2. Revisar los tipos de datos
#    a. numeric : + - * / %
#    b. string  : + (concatenar)
#    c. boolean : ! || &&
#    d. void    : comparacion (==, !=)
#
# 3. Control de flujo
#    a. Debe de existir una funcion main                   update: Listo
#    b. toda funcion debe de tener al menos un return      update: Listo
#    c. las instrucciones break/continue deben de estar    update: Listo
#       definidas dentro de un while/for
#
# ---------------------------------------------------------------------

from AST import *
from colorama import init, Fore, Back, Style

class Symtab:

    class SymbolDefinedError(Exception):
        pass
        
    def __init__(self, parent=None, name=None, lineno=0):
        self.name = name
        self.entries = {}
        self.parent = parent
        self.bealoop = False
        self.Return = False 
        self.lieneo = lineno
        if self.parent:
            self.parent.children.append(self)
        self.children = []

        exception = ["While", "For", "If", "Global"]
        if name in exception:
            self.Return = True

    def haveReturn(self):
        self.Return = True

    def checkReturn(self):
        for child in self.children:
            child.checkReturn()
        if not self.Return:
            print("\x1b[1;31m"+self.name+"\x1b[0;31m"+f" no tiene almenos un return, linea: {self.lieneo}"+Fore.RESET )
            # print( "no: ",self.name)
        return False
    
    def printenv(self):
        for child in self.children:
            child.printenv()
        print(" ", self.name, ": ", self.Return)
        for i in self.entries:
            print("   ", i)

    def iamaloop(self):
        self.bealoop = True
        
    def add(self, str, value):
        if str in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[str] = value
    
    def amialoop(self):
        if self.bealoop:
            return True
        elif self.parent:
            return self.parent.amialoop()
        return False

    def get(self, name):
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None

class Checker(Visitor):
    def __init__(self):
        self.curr_symtab = Symtab()

    def _add_symbol(self, node, value, env: Symtab, lineno=0):
        try:
            env.add(value, node)
        except Symtab.SymbolDefinedError:
            self.error(f"Simbolo " +"\x1b[1;31m"+ f"'{value}'"+"\x1b[0;31m"+ f" ya previamente definido, line: {lineno}")

    def error(self, text):
        print(Fore.RED+text+Fore.RESET)

    @classmethod
    def check(cls, model, symtable):
        checker = cls()
        cls.symtable = symtable
        model.accept(checker, Symtab(name="Global"))
        return checker
        
    def visit(self, node: TranslationUnit, env: Symtab):
        for decl in node.decls:
            decl.accept(self, env)    
        if not "main" in env.entries:
            self.error(f"No existe funcion " + "\x1b[1;31m" +"main")
        env.checkReturn()
        if self.symtable: 
            print("\nTabla de simbolos: ")
            env.printenv()

    def visit(self, node: FuncDeclaration, env: Symtab):
        name = node.params.accept(self, None)
        self._add_symbol(node, name, env, node.lineno)
        newenv = Symtab(env, name, node.lineno)
        node.params.accept(self, newenv)

        for stmt in node.body:
            stmt.accept(self, newenv)         

    def visit(self, node: FuncDeclarationStmt, env):
        if env == None:
            return node.name
        for stmt in node.body:
            stmt.accept(self, env)
        
    def visit(self, node: TypeDeclaration, env: Symtab):
        self._add_symbol(node, node.body, env, node.lineno)

    def visit(self, node: Parameter_declaration, env: Symtab):
        for stmt in node.decls:
            stmt.accept(self, env)

    def visit(self, node: VarDeclaration, env: Symtab):
        if type(node.expr) == str:
            self._add_symbol(node, node.expr, env, node.lineno)
        else: 
            node.expr.accept(self, env)
        
    def visit(self, node: WhileStmt, env: Symtab):
        newenv = Symtab(env, "While")
        newenv.iamaloop()
        node.cond.accept(self, newenv)
        for stmt in node.body:
            stmt.accept(self, newenv)
    
    def visit(self, node: For, env: Symtab):
        newenv = Symtab(env, "For")
        newenv.iamaloop()
        if node.init:
            node.init.accept(self, newenv)
        if node.expr:
            node.expr.accept(self, newenv)
        if node.post:
            node.post.accept(self, newenv)
        for stmt in node.stmts:
            stmt.accept(self, newenv)
    
    def visit(self, node: IfStmt, env: Symtab):
        newenv = Symtab(env, "If")
        node.cond.accept(self, newenv)
        for param in node.cons:
            param.accept(self, newenv)
        for param in node.altr:
            param.accept(self, newenv)

    def visit(self, node: Return, env: Symtab):
        env.haveReturn()
        if node.expr:
            node.expr.accept(self, env)
    
    def visit(self, node: Break, env: Symtab):
        if not env.amialoop():
            self.error(f"\x1b[1;31m" + "Break" + "\x1b[0;31m" +f" no esta dentro de un For/While, linea: {node.lineno}")
        
    def visit(self, node: Binary, env: Symtab):
        node.left.accept(self, env)
        node.right.accept(self, env)
        
    def visit(self, node: Unary, env: Symtab):
        node.expr.accept(self, env)
 
    def visit(self, node: Call, env: Symtab):

       # node.func.accept(self, env)
        for param in node.args:
            param.accept(self, env)
        
    def visit(self, node: ID, env: Symtab):
        value = env.get(node.name)
        if value is None:
            self.error(f'La Variable '+ "\x1b[1;31m" + f"{node.name}" + "\x1b[0;31m" + f' no esta definida, linea: {node.lineno}')
            
    def visit(self, node: INUMBER, env: Symtab):
        pass
    
    def visit(self, node: FNUMBER, env: Symtab):
        pass
    
    def visit(self, node: CONST, env: Symtab):
        pass

    def visit(self, node: Continue, env: Symtab):
        if not env.amialoop():
            self.error(f"\x1b[1;31m" + "Continue" + "\x1b[0;31m" + f" no esta dentro de un For/While, linea: {node.lineno}")
    
    def visit(self, node: CHARACTER, env: Symtab):
        pass
    
    def visit(self, node: string_literal, env: Symtab):
        pass
    
    def visit(self, node: Array, env: Symtab):
        node.expr.accept(self, env)
        node.index.accept(self, env)
