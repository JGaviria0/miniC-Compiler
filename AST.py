

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
class Continue(Statement):
	name  :  str

@dataclass
class Break(Statement):
	name  :  str
	
@dataclass
class CompoundStmt(Statement):
	stmts: List[Statement]=field(default_factory=list)
	
@dataclass
class NullStmt(Statement):
	name: str=';'

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

@dataclass
class ConstDeclaration(Declaration):
    name: str
    value: Expression

@dataclass
class FuncDeclarationStmt(Statement):
	name: str
	body: List[Statement]=field(default_factory=list)
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
    
    def visit(self, n:FuncDeclaration):
        name = self.name()
        self.dot.node(name, label="Func\\nDeclaration{n.Static} ")
        return name

   # def visit(self, n:Unary):
    #    name = self.name()
     #   self.dot.node(name, label=f"Unary\\nop='{n.op}")
      #  self.dot.edge(name, n.expr.accept(self))
       # return name

  #  def visit(self, n:Variable):
   #     name = self.name()
    #    self.dot.node(name, label=f"Ident\\nname='{n.name}")
     #   return name
