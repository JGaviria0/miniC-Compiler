

from dataclasses import dataclass,field
from multimethod import multimeta
import graphviz as gpv
from typing import Any, List

class Visitor(metaclass=multimeta):
	pass

@dataclass
class Node:
	def accept(self, vis: Visitor,*args,**kwargs):
		return vis.visit(self,*args,**kwargs)
	

#-----------------------------------------------------

#-----------------------------------------------------------------
#Nodos
#----------------------------------------------------------------

@dataclass
class Statement(Node):
	'''expresiones sin valor asosciado'''
	pass

@dataclass
class Expression(Node):
	'''nodos que representan valores'''
	pass


@dataclass
class Declaration(Statement):
	pass


#------------------------------------------------------------
#Statements
#------------------------------------------------------------

@dataclass
class Return(Statement):
  expr: List[Expression] = field(default_factory=list)

@dataclass
class ID(Node):
    name : str
    lineno: int = 0

@dataclass
class INUMBER(Node):
    name : str

@dataclass
class FNUMBER(Node):
    name : str

@dataclass
class CONST(Node):
    name : str

@dataclass
class CHARACTER(Node):
    name : str

@dataclass
class string_literal(Node):
    name : str


@dataclass
class IfStmt(Statement):
    cond   : Expression
    cons   : List [Statement]=field(default_factory=list)
    altr   : List [Statement]=field(default_factory=list)

@dataclass
class WhileStmt(Statement):
	cond: Expression
	body: List[Statement]=field(default_factory=list)


@dataclass
class For(Statement):
  init : Statement
  expr : Expression
  post : Statement
  stmts: List[Statement]=field(default_factory=list)

@dataclass
class Continue(Statement):
	lineno: int = 0

@dataclass
class Break(Statement):
	lineno: int = 0
	
@dataclass
class CompoundStmt(Statement):
	stmts: List[Statement]=field(default_factory=list)
	
@dataclass
class NullStmt(Statement):
	name: str=';'


@dataclass
class Parameter(Declaration):
  int : str
  name: str
#------------------------------------------------------------
#Expression
#------------------------------------------------------------

@dataclass
class Unary(Expression):
	op: str
	expr: Expression
	
@dataclass
class Binary(Expression):
	left : Expression
	op   : str
	right: Expression


@dataclass
class Return(Statement):
    expr: Expression = None
    lineno: int = 0
	
@dataclass
class Literal(Expression):
	value: Any

	
@dataclass
class Variable(Literal):
    name: str
    
@dataclass
class Call(Expression):
	func: str
	args: List[Expression] = field(default_factory=list)
	
@dataclass
class Array(Expression):
  expr : Expression
  index: Expression
	
	

#------------------------------------------------------------
#Declaration
#------------------------------------------------------------

@dataclass
class FuncDeclaration(Declaration):
	name: str
	params: List[Expression]=field(default_factory=list)
	body: List[Statement]=field(default_factory=list)
	Static:bool=False
	lineno: int = 0

@dataclass
class VarDeclaration(Declaration):
	name: str
	expr: Expression
	Ext:bool=False
	Static : bool = False
	lineno: int = 0

@dataclass
class ConstDeclaration(Declaration):
    name: str
    value: Expression
    
@dataclass
class TypeDeclaration(Statement):
    Type: str
    body: Statement
    lineno: int = 0

@dataclass
class FuncDeclarationStmt(Statement):
	name: str
	body: List[Statement]=field(default_factory=list)

@dataclass
class TranslationUnit(Statement):
	decls : List[Statement]

@dataclass
class Parameter_declaration(Statement):
	decls : List[Statement]



@dataclass
class ParamList(Declaration):
    params  : List[Parameter]
    ellipsis: bool = False



# ----------------------------------------
# Expression representan valores
#


class RenderAST(Visitor):
    node_default = {
        'shape' : 'box',
        'color' : 'deepskyblue',
        'style' : 'filled',
    }
    edge_default = {
        'arrowhead' : 'none'
    }

    def __init__(self):
        self.dot = gpv.Digraph('AST', comment='Dot')
        self.dot.attr('node', **self.node_default)
        self.dot.attr('edge', **self.edge_default)
        self.seq = 0
    
    def name(self):
        self.seq += 1
        return f'n{self.seq:02d}'

    @classmethod
    def render(cls, n:Node):
        dot = cls()
        n.accept(dot)
        return dot.dot
    
    def visit(self, n:TranslationUnit):
        name = self.name()
        self.dot.node(name, label='Funcion')
        for i in n.decls:
            self.dot.edge(name, i.accept(self))

    def visit(self, n:FuncDeclaration):
        name = self.name()
        self.dot.node(name, label=f"Func Declaration\ntype:{n.name} \nexternal:{n.Static}\n")
        self.dot.edge(name, n.params.accept(self))
        for i in n.body:
            self.dot.edge(name, i.accept(self))
        return name
    def visit(self, n:FuncDeclarationStmt):
        name = self.name()
        self.dot.node(name, label=f"Funcion \nname:{n.name} \n")
        for i in n.body:
            self.dot.edge(name, i.accept(self))
        return name
    def visit(self, n:TypeDeclaration):
        name = self.name()
        if type(n.body) != str:
            self.dot.node(name, label=f"Param\nType:{n.Type} \n")
            self.dot.edge(name, n.body.accept(self))
        else: 
             self.dot.node(name, label=f"Param\nType:{n.Type} \n name:{n.body}")
        return name
    
    def visit(self, n:Parameter_declaration):
        name = self.name()
        self.dot.node(name, label='ParamDeclaracion')
        for i in n.decls:
            self.dot.edge(name, i.accept(self))
    
    def visit(self, n:VarDeclaration):
        name = self.name()
        if type(n.expr ) != str: 
            self.dot.node(name, label=f'Var declaration\ntype: {n.name}')
            self.dot.edge(name, n.expr.accept(self))
        else: 
            self.dot.node(name, label=f'Var declaration\ntype: {n.name}\nname: {n.expr}')
        return name
    
    def visit(self, n:WhileStmt):
        name = self.name()
        self.dot.node(name, label=f'while\cond: ')
       
        self.dot.edge(name, n.cond.accept(self))
        for i in n.body:
            self.dot.edge(name, i.accept(self))
        
        return name
    
    def visit(self, n:For):
        name = self.name()
        self.dot.node(name, label=f'For\cond: ')
       
        self.dot.edge(name, n.init.accept(self))
        self.dot.edge(name, n.expr.accept(self))
        self.dot.edge(name, n.post.accept(self))
        for i in n.stmts:
            self.dot.edge(name, i.accept(self))
        
        return name
     
    def visit(self, n:IfStmt):
        name = self.name()
        self.dot.node(name, label=f'If\cond: ')
        self.dot.edge(name, n.cond.accept(self))
        for i in n.cons:
            self.dot.edge(name, i.accept(self))

        for i in n.altr:
            self.dot.edge(name, i.accept(self),label=f'Else:')
        
        return name


    def visit(self, n:Unary):
        name = self.name()
        self.dot.node(name, label=f"Unary\\nop={n.op}")
        self.dot.edge(name, n.expr.accept(self))
        return name
    
    def visit(self, n:Binary):
        name = self.name()
        self.dot.node(name, label=f"Binary\\nop:{n.op}")
        self.dot.edge(name, n.left.accept(self))
        self.dot.edge(name, n.right.accept(self))
        return name

    def visit(self, n:Variable):
        name = self.name()
        self.dot.node(name, label=f"Ident\\nname={n.name}")
        return name
    
    def visit(self, n:Break):
        name = self.name()
        self.dot.node(name, label=f"Break")
        return name
    
    def visit(self, n:Continue):
        name = self.name()
        self.dot.node(name, label=f"Continue")
        return name
    
    def visit(self, n:ID):
        name = self.name()
        self.dot.node(name, label=f"ID={n.name}")
        return name
    
    def visit(self, n:INUMBER):
        name = self.name()
        self.dot.node(name, label=f"INUMBER={n.name}")
        return name
    
    def visit(self, n:FNUMBER):
        name = self.name()
        self.dot.node(name, label=f"FNUMBER={n.name}")
        return name
    
    def visit(self, n:CONST):
        name = self.name()
        self.dot.node(name, label=f"CONST={n.name}")
        return name
    
    def visit(self, n:CHARACTER):
        name = self.name()
        self.dot.node(name, label=f"CHARACTER={n.name}")
        return name
    
    def visit(self, n:string_literal):
        name = self.name()
        self.dot.node(name, label=f"string literal={n.name}")
        return name
    
    def visit(self, n:Return):
        name = self.name()
        self.dot.node(name, label=f"Return:")
        if n.expr:
            self.dot.edge(name, n.expr.accept(self))
        return name
    
    def visit(self, n:Call):
        name = self.name()
        self.dot.node(name, label=f"Call")
        self.dot.edge(name, n.func.accept(self))
        for i in n.args:
            self.dot.edge(name, i.accept(self))
        return name
    
    def visit(self, n:Array):
        name = self.name()
        self.dot.node(name, label=f"Array")
        self.dot.edge(name, n.expr.accept(self))
        self.dot.edge(name, n.index.accept(self))
        
        return name