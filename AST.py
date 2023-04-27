

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
class node_test(Node):
    name : str

@dataclass
class ID(Node):
    name : str

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
class ExprStmt(Statement):
	expr: Expression
	
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
	pass

@dataclass
class Break(Statement):
	pass
	
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
class Assign(Expression):
	name : str
	opr: str

@dataclass
class Return(Statement):
	expr: Expression
	
@dataclass
class Literal(Expression):
	value: Any
	
@dataclass
class Call(Expression):
	func: str
	args: List[Expression] = field(default_factory=list)
	
	
@dataclass
class Array(Expression):
	name: str
	args: List[Expression] = field(default_factory=list)
	
	
@dataclass
class Logical(Expression):
	op   : str
	left : Expression
	right: Expression
#------------------------------------------------------------
#Declaration
#------------------------------------------------------------

@dataclass
class FuncDeclaration(Declaration):
	name: str
	params: List[Expression]=field(default_factory=list)
	body: List[Statement]=field(default_factory=list)
	Static:bool=False

@dataclass
class VarDeclaration(Declaration):
	name: str
	expr: Expression
	end:str
	Ext:bool=False
	Static : bool = False

@dataclass
class ConstDeclaration(Declaration):
    name: str
    value: Expression
    
@dataclass
class TypeDeclaration(Statement):
    Type: str
    body: Statement

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


@dataclass
class Variable(Literal):
  name: str
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
        self.dot.node(name, label='decls')
        for i in n.decls:
            self.dot.edge(name, i.accept(self))

    def visit(self, n:FuncDeclaration):
        name = self.name()
        self.dot.node(name, label=f"Func Declaration\ntype:{n.name} \nexternal:{n.Static}\n")
        self.dot.edge(name, n.params.accept(self))
        for i in n.body:
            print(i)
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
        self.dot.node(name, label=f"Param\nType:{n.Type} \n name:{n.body}")
        return name
    def visit(self, n:Parameter_declaration):
        name = self.name()
        self.dot.node(name, label='decls')
        for i in n.decls:
            self.dot.edge(name, i.accept(self))
    
    def visit(self, n:VarDeclaration):
        name = self.name()
        self.dot.node(name, label=f'Var declaraiton\ntype: {n.name}\nexpr: {n.expr}')
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
    
    def visit(self, n:node_test):
        name = self.name()
        self.dot.node(name, label=f"node test={n.name}")
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
