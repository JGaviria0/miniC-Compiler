from AST import *

class Symtab:

    class SymbolDefinedError(Exception):
        pass
        
    def __init__(self, parent=None):
        self.entries = {}
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
        self.children = []
        
    def add(self, str, value):
        if str in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[str] = value
        
    def get(self, name):
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None


class Checker(Visitor):
    def __init__(self):
        self.curr_symtab = Symtab()

    def _add_symbol(self, node, value, env: Symtab):
        try:
            self.curr_symtab.add(value, node)
            
            print(self.curr_symtab.entries, '\n\n\n\n')
            
        except Symtab.SymbolDefinedError:
            self.error(f"Simbol '{value}'  ya previamente esta definido.")

   
    def error(self, text):
        print(text)
    @classmethod
    def check(cls, model):
        checker = cls()
        model.accept(checker, Symtab())
        return checker
        
    def visit(self, node: TranslationUnit, env: Symtab):
        for decl in node.decls:
            decl.accept(self, env)

    def visit(self, node: FuncDeclaration, env: Symtab):
        name = node.params.accept(self, None)
        self._add_symbol(node, name, env)
        newenv = Symtab(env)
        node.params.accept(self, newenv)

        for stmt in node.body:
            stmt.accept(self, newenv)
        try:
            print(name, env.entries)
        except: 
            pass

    def visit(self, node: FuncDeclarationStmt, env):
        if env == None:
            return node.name
        for stmt in node.body:
            stmt.accept(self, env)
            
        # print("envFunc2: ", env.entries, env.parent, env.children)

    def visit(self, node: TypeDeclaration, env: Symtab):
        self._add_symbol(node, node.body, env)

    
    def visit(self, node: Parameter_declaration, env: Symtab):
        for stmt in node.decls:
            stmt.accept(self, env)


    def visit(self, node: VarDeclaration, env: Symtab):
        self._add_symbol(node, node.expr, env)
        
    def visit(self, node: WhileStmt, env: Symtab):
    
        node.cond.accept(self, env)
        for stmt in node.body:
            stmt.accept(self, env)
    
    def visit(self, node: For, env: Symtab):
    
        if node.init:
            node.init.accept(self, env)
        if node.expr:
            node.expr.accept(self, env)
        if node.post:
            node.post.accept(self, env)
        for stmt in node.stmts:
            stmt.accept(self, env)
    
    def visit(self, node: IfStmt, env: Symtab):
        newenv = Symtab(env)
        node.cond.accept(self, newenv)
        for param in node.cons:
            param.accept(self, newenv)
        for param in node.altr:
            param.accept(self, newenv)

    def visit(self, node: Return, env: Symtab):
        if node.expr:
            node.expr.accept(self, env)
        
    def visit(self, node: Binary, env: Symtab):
        node.left.accept(self, env)
        node.right.accept(self, env)
        
    def visit(self, node: Unary, env: Symtab):
        node.expr.accept(self, env)
        
    def visit(self, node: Variable, env: Symtab):
        '''
        1. Buscar nombre en la tabla de simbolos (contexto actual)
        '''
        
        value = env.get(node.name)
        print(value)
        if value is None:
            print(f'La Variable {node.name} no esta definida')
        
 
    def visit(self, node: Call, env: Symtab):

       # node.func.accept(self, env)
        for param in node.args:
            param.accept(self, env)
        

    def visit(self, node: node_test, env: Symtab):
       pass
        
    def visit(self, node: ID, env: Symtab):
        pass
    
    def visit(self, node: INUMBER, env: Symtab):
        pass
    
    def visit(self, node: FNUMBER, env: Symtab):
        pass
    
    def visit(self, node: CONST, env: Symtab):
        pass
    
    def visit(self, node: CHARACTER, env: Symtab):
        pass
    
    def visit(self, node: string_literal, env: Symtab):
        pass
    
    def visit(self, node: Array, env: Symtab):
        node.expr.accept(self, env)
        node.index.accept(self, env)
