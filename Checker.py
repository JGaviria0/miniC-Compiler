from typing import Union
from AST import *

class Symtab:
    
    class SymbolDefinedError(Exception):
        pass

    class SymbolConflictError(Exception):
        pass
        
    def __init__(self, parent=None):
        self.entries = {}
        self.parent = parent
        if self.parent:
            self.parent.children.append(self)
        self.children = []
        
    def add(self, name, value):
        if name in self.entries:
            raise Symtab.SymbolDefinedError()
        self.entries[name] = value
        
    def get(self, name):
        if name in self.entries:
            return self.entries[name]
        elif self.parent:
            return self.parent.get(name)
        return None


class Checker(Visitor):
    def __init__(self):
        self.curr_symtab = Symtab()

    def push_symtab(self, node):
        self.curr_symtab = Symtab(self.curr_symtab)
        node.symtab = self.curr_symtab

    def pop_symtab(self):
        self.curr_symtab = self.curr_symtab.parent

    def _add_symbol(self, node, env: Symtab):
        try:
            self.curr_symtab.add(node.name, node)
        except Symtab.SymbolDefinedError:
            self.error(f"Symbol '{node.name}' is already defined.")
        except Symtab.SymbolConflictError:
            self.error(f"Symbol '{node.name}' has multiple conflicting declarations.")

    def error(self, text):
        print(text)

    @classmethod
    def check(cls, model):
        checker = cls()
        model.accept(checker, Symtab())
        return checker
    
    def visit(self, node: TranslationUnit, env: Symtab):
        pass

    def visit(self, node: FuncDeclaration, env: Symtab):
        self._add_symbol(node, env)
        env = Symtab(env)
        for param in node.params:
            self._add_symbol(VarDeclaration(param), env)
        for stmt in node.stmts:
            stmt.accept(self, env)
        if not any(isinstance(stmt, Return) for stmt in node.stmts):
            self.error(f"Function '{node.name}' is missing a return statement.")

    def visit(self, node: VarDeclaration, env: Symtab):
        self._add_symbol(node, env)
        if node.expr:
            node.expr.accept(self, env)

    def visit(self, node: IfStmt, env: Symtab):
        node.test.accept(self, env)
        node.cons.accept(self, env)
        if node.altr:
            node.altr.accept(self, env)

    def visit(self, node: WhileStmt, env: Symtab):
        node.test.accept(self, env)
        for stmt in node.body:
            stmt.accept(self, env)

    def visit(self, node: Return, env: Symtab):
        node.expr.accept(self, env)

    def visit(self, node: Literal, env: Symtab):
        pass

    def visit(self, node: Binary, env: Symtab):
        node.left.accept(self, env)
        node.right.accept(self, env)

    def visit(self, node: Unary, env: Symtab):
        node.expr.accept(self, env)

    def visit(self, node: Variable, env: Symtab):
        value = env.get(node.name)
        if value is None:
            self.error(f"Variable '{node.name}' is not defined.")

    def visit(self, node: Call, env: Symtab):
        function = env.get(node.name)
        if function is None:
            self.error(f"Function '{node.name}' is not defined.")
        else:
            if not isinstance(function, FuncDeclaration):
                self.error(f"'{node.name}' is not a function.")
            else:
                if len(node.args) != len(function.params):
                    self.error(f"Invalid number of arguments for function '{node.name}'.")
                else:
                    for arg, param in zip(node.args, function.params):
                        arg.accept(self, env)
                        param.accept(self, env)
