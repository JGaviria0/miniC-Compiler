import logging
import sly
from AST import *
from rich import print as rprint
from Lexer import Lexer


class Parser(sly.Parser):
	debugfile = "minic.txt"

	tokens = Lexer.tokens
	

	@_("translation_unit")
	def program(self, p):
		return TranslationUnit(p.translation_unit)

	@_("external_declaration")
	def translation_unit(self, p):
		return [p.external_declaration]

	@_("translation_unit external_declaration")
	def translation_unit(self, p):
		return p.translation_unit+[p.external_declaration]

	@_("function_definition")
	def external_declaration(self, p):
		return p.function_definition
	
	@_("declaration")
	def external_declaration(self, p):
		return p.declaration
		

	@_("type_specifier declarator compound_statement")
	def function_definition(self, p):
		return FuncDeclaration(p.type_specifier,p.declarator,p.compound_statement)
		

	@_("STATIC type_specifier declarator compound_statement")
	def function_definition(self, p):
		return FuncDeclaration(p.type_specifier,p.declarator,p.compound_statement,Static=True)
		

	@_("type_specifier declarator ';'")
	def declaration(self, p):
		return VarDeclaration(p.type_specifier, p.declarator, p[2])
		
	@_("EXTERN type_specifier declarator ';'")
	def declaration(self, p):
		return VarDeclaration(p.type_specifier,p.declarator,p[3],Ext=True)
		
	@_("empty")
	def declaration_list_opt(self, p):
		return []
		
	@_("declaration_list")
	def declaration_list_opt(self, p):
		return p.declaration_list
		
	@_("declaration")
	def declaration_list(self, p):
		return  [p.declaration]
		
#....	
	@_("declaration_list declaration")
	def declaration_list(self, p):
		return p.declaration_list+[p.declaration]
		
	@_("INT", "FLOAT", "CHAR", "VOID")
	def type_specifier(self, p):
		return p[0]
		
	@_("direct_declarator")
	def declarator(self, p):
		return p.direct_declarator
		
	@_("'*' declarator")
	def declarator(self, p):
		return node_test("declarator")
		
	@_("ID")
	def direct_declarator(self, p):
		return p[0]
		
	@_("direct_declarator '(' parameter_type_list ')'")
	def direct_declarator(self, p):
		return FuncDeclarationStmt(p.direct_declarator,p.parameter_type_list)
		
	@_("direct_declarator '(' ')'")
	def direct_declarator(self, p):
		return FuncDeclarationStmt(p.direct_declarator,[])
		
	@_("parameter_list")
	def parameter_type_list(self, p):
		return p.parameter_list
		
	@_("parameter_list ',' ELLIPSIS")
	def parameter_type_list(self, p):
		#return Trinary_V2(p.parameter_list,p[1],p[2])
		pass
	@_("parameter_declaration")
	def parameter_list(self, p):
		return [p.parameter_declaration]
		
	@_("parameter_list ',' parameter_declaration")
	def parameter_list(self, p):
		return p.parameter_list+[p.parameter_declaration]
		
	@_("type_specifier declarator")
	def parameter_declaration(self, p):
		return TypeDeclaration(p.type_specifier,p.declarator)
		
	@_("'{' declaration_list_opt statement_list '}'")
	def compound_statement(self, p):
		return p.declaration_list_opt + p.statement_list
		

	@_("'{' declaration_list_opt '}'")
	def compound_statement(self, p):
		return p.declaration_list_opt
	
	@_("expression ';'")
	def expression_statement(self, p):
		#return Unary(p[1],p.expression)
		print(f'entre aaqui? {p.expression}')
		return p.expression
	
	@_("equality_expression")
	def expression(self, p):
		return p.equality_expression
		
	@_("assigment_expression")
	def expression(self, p):
		print(f"es un assigment 134 equ_:{p.assigment_expression} ")

		return p.assigment_expression
		


	@_("equality_expression '='   expression",
	   "equality_expression ADDEQ expression",
	   "equality_expression MODEQ expression",
	   "equality_expression DIVEQ expression",
	   "equality_expression MULEQ expression",
	   "equality_expression SUBEQ expression")
	def assigment_expression(self, p):
		print(f"es un assigment 145 equ_:{p.equality_expression} expr: {p.expression}")
		return Binary(p.equality_expression,p[1],p.expression)
		
	@_("relational_expression")
	def equality_expression(self, p):
		return p.relational_expression
		
	@_("equality_expression EQ relational_expression",
	   "equality_expression NE relational_expression")
	def equality_expression(self, p):
		return Binary(p.equality_expression,p[1],p.relational_expression)
		
	@_("additive_expression")
	def relational_expression(self, p):
		return p.additive_expression
		
	@_("relational_expression '<' additive_expression",
    	"relational_expression LT additive_expression",
	    "relational_expression GT additive_expression",
	   "relational_expression LE  additive_expression",
	   "relational_expression '>' additive_expression",
	   "relational_expression LOR additive_expression",
	   "relational_expression LAND additive_expression",
	   "relational_expression GE  additive_expression")
	def relational_expression(self, p):
		
		return Binary(p.relational_expression,p[1],p.additive_expression)

		
	@_("primary_expression")
	def postfix_expression(self, p):
		return p.primary_expression
		
	@_("postfix_expression '(' argument_expression_list ')'")
	def postfix_expression(self, p):
		#return Quadnary_v4(p.postfix_expression,p[1],p.argument_expression_list,p[3])
		pass
	@_("postfix_expression '(' ')'")
	def postfix_expression(self, p):
		#return Trinary_V3(p.postfix_expression,p[1],p[2])
		pass
	@_("postfix_expression '[' expression ']'")
	def postfix_expression(self, p):
		#return Quadnary_v4(p.postfix_expression,p[1],p.expression,p[3])
		pass
	@_("expression")
	def argument_expression_list(self, p):
		#return p.expression
		pass
	@_("argument_expression_list ',' expression")
	def argument_expression_list(self, p):
		#return Binary(p.argument_expression_list,p[1],p.expression)
		pass
	@_("postfix_expression")
	def unary_expression(self, p):
		return p.postfix_expression
		
	@_("'-' unary_expression")
	def unary_expression(self, p):
		#return Unary(p[0],p.unary_expression)
		pass
	@_("'+' unary_expression")
	def unary_expression(self, p):
		#return Unary(p[0],p.unary_expression)
		pass
	@_("'!' unary_expression")
	def unary_expression(self, p):
		#return Unary(p[0],p.unary_expression)
		pass
	@_("'*' unary_expression")
	def unary_expression(self, p):
		#return Unary(p[0],p.unary_expression)
		pass
	@_("'&' unary_expression")
	def unary_expression(self, p):
		#return Unary(p[0],p.unary_expression)
		pass
	@_("unary_expression")
	def mult_expression(self, p):
		return p.unary_expression
		
	@_("mult_expression '*' unary_expression",
	   "mult_expression '/' unary_expression",
	   "mult_expression '%' unary_expression")
	def mult_expression(self, p):
		return Binary(p.mult_expression,p[1],p.unary_expression)
		
	@_("mult_expression")
	def additive_expression(self, p):
		return p.mult_expression
		
	@_("additive_expression '+' mult_expression",
	   "additive_expression '-' mult_expression")
	def additive_expression(self, p):
		return Binary(p.additive_expression,p[1],p.mult_expression)
		
	@_("ID")
	def primary_expression(self, p):
		
		return ID(p[0])
		
	@_("INUMBER")
	def primary_expression(self, p):
		
		return INUMBER(p[0])
	@_("FNUMBER")
	def primary_expression(self, p):
		
		return FNUMBER(p[0])
	@_("CONST")
	def primary_expression(self, p):
		
		return CONST(p[0])
	@_("CHARACTER")
	def primary_expression(self, p):
		
		return CHARACTER(p[0])
	@_("string_literal")
	def primary_expression(self, p):
		return string_literal(p[0])
		
	@_("'(' expression ')'")
	def primary_expression(self, p):
		#return Trinary_V3(p.expression,p[0],p[2])
		pass

	@_("STRING")
	def string_literal(self, p):
		#return Variable(p[0])
		pass

	@_("string_literal STRING")
	def string_literal(self, p):
	#	return ConstDeclaration(p[1],p.string_literal)
		pass

	@_("RETURN ';'")
	def jumpstatement(self, p):
		#return Assign(p[0],p[1])
		pass
	@_("RETURN expression ';'")
	def jumpstatement(self, p):
		#return Trinary_V3(p.expression,p[0],p[2])
		pass
	@_("BREAK ';'")
	def jumpstatement(self, p):
		#return Assign(p[0],p[1])
		pass
	@_("CONTINUE ';'")
	def jumpstatement(self, p):
		#return Assign(p[0],p[1])
		pass
	@_("open_statement")
	def statement(self, p):
		return p.open_statement 
		
	@_("closed_statement")
	def statement(self, p):
		return p.closed_statement 
		
	@_("compound_statement")
	def other_statement(self, p):
		return p.compound_statement
		
	@_("expression_statement")
	def other_statement(self, p):
		return p.expression_statement
		
	@_("jumpstatement")
	def other_statement(self, p):
		#return p.jumpstatement
		pass

	@_("WHILE '(' expression ')' open_statement")
	def open_statement(self, p):
		
		return WhileStmt( p.expression, p.open_statement )
    
    
	@_("WHILE '(' expression ')' closed_statement")
	def closed_statement(self, p):
		
		return WhileStmt( p.expression, p.closed_statement )

	@_("IF '(' expression ')' closed_statement ELSE open_statement")
	def open_statement(self, p):
		return IfStmt(p.expression, p.closed_statement, p.open_statement)

	@_("IF '(' expression ')' closed_statement ELSE closed_statement")
	def closed_statement(self, p):
		return IfStmt(p.expression, p.closed_statement0, p.closed_statement1)

	@_("IF '(' expression ')' open_statement")
	def open_statement(self, p):
		return IfStmt(p.expression, p.open_statement)
    
	@_("IF '(' expression ')' other_statement")
	def open_statement(self, p):
		return IfStmt(p.expression, p.other_statement)

	

	@_("FOR '(' expression_statement expression_statement expression ')' open_statement")
	def open_statement(self, p):
		return For( p.expression_statement0, p.expression_statement1, p.expression, p.open_statement )

	@_("FOR '(' expression_statement expression_statement expression ')' closed_statement")
	def closed_statement(self, p):
		return For( p.expression_statement0, p.expression_statement1, p.expression, p.closed_statement )


	@_("other_statement")
	def closed_statement(self, p):
		return p.other_statement
		



	@_("statement")
	def statement_list(self, p):
		return [p.statement]
		

	@_("statement_list statement")
	def statement_list(self, p):
		return p.statement_list + [p.statement]

	@_("")
	def empty(self, p):
		pass

	def error(self, p):
		lineno = p.lineno if p else 'EOF'
		value  = p.value  if p else 'EOF'
		print(f"{lineno}: Error de Sintaxis en {value}")
		raise SyntaxError()
	

if __name__ == '__main__':
	import sys
	
	if len(sys.argv) != 2:
		print(f"usage: python {sys.argv[0]} fname")
		exit(1)
	
	l = Lexer()
	
	p = Parser()
	txt = open(sys.argv[1], encoding='utf-8').read()

	ast = p.parse(l.tokenize(txt))
	dot = RenderAST.render(ast)
	print("Archivo minic.txt creado con exito")
	print(ast)

	f = open('tree.dot','w')
	f.write(str(dot))
	f.close()