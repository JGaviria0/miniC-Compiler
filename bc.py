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
		#return VarDeclaration(p.type_specifier, p.declarator, p[2])
		if isinstance(p.declarator, tuple):
			return FuncDeclarationStmt( p.type_specifier,p.declarator)
		else:
			return VarDeclaration(p.type_specifier, p.declarator,p[2])
		
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
		pass
		
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
		
		#return ParamList(p.parameter_list)
		pass	
	@_("parameter_list ',' ELLIPSIS")
	def parameter_type_list(self, p):
		pass
		#return ParamList(p.parameter_list, ellipsis=True)
		
	@_("parameter_declaration")
	def parameter_list(self, p):
		pass
		#return [p.parameter_declaration]
		
	@_("parameter_list ',' parameter_declaration")
	def parameter_list(self, p):
		#return p.parameter_list+[p.parameter_declaration]
		pass
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
		return Unary(p[1],p.expression)
		
	@_("equality_expression")
	def expression(self, p):
		return p.equality_expression
		
	@_("assigment_expression")
	def expression(self, p):
		return p.assigment_expression
		


	@_("equality_expression '='   expression",
	   "equality_expression ADDEQ expression",
	   "equality_expression MODEQ expression",
	   "equality_expression DIVEQ expression",
	   "equality_expression MULEQ expression",
	   "equality_expression SUBEQ expression")
	def assigment_expression(self, p):
	#	return Binary(p.equality_expression,p[1],p.expression)
		pass	
	@_("relational_expression")
	def equality_expression(self, p):
		return p.relational_expression
		
	@_("equality_expression EQ relational_expression",
	   "equality_expression NE relational_expression")
	def equality_expression(self, p):
		#return Binary(p.equality_expression,p[1],p.relational_expression)
		pass
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
		#Binary(p.relational_expression,p[1],p.additive_expression)
		pass
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
		#return p.postfix_expression
		pass
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
		#return p.unary_expression
		pass
	@_("mult_expression '*' unary_expression",
	   "mult_expression '/' unary_expression",
	   "mult_expression '%' unary_expression")
	def mult_expression(self, p):
		#return Binary(p.mult_expression,p[1],p.unary_expression)
		pass
	@_("mult_expression")
	def additive_expression(self, p):
		#return p.mult_expression
		pass
	@_("additive_expression '+' mult_expression",
	   "additive_expression '-' mult_expression")
	def additive_expression(self, p):
		#return Binary(p.additive_expression,p[1],p.mult_expression)
		pass
	@_("ID")
	def primary_expression(self, p):
		#return Variable(p[0])
		pass
	@_("INUMBER")
	def primary_expression(self, p):
		#return Variable(p[0])
		pass
	@_("FNUMBER")
	def primary_expression(self, p):
		#return Variable(p[0])
		pass
	@_("CONST")
	def primary_expression(self, p):
		#return Variable(p[0])
		pass
	@_("CHARACTER")
	def primary_expression(self, p):
		#return Variable(p[0])
		pass
	@_("string_literal")
	def primary_expression(self, p):
		#return p.string_literal
		pass
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
		return VarDeclaration(name='int', expr='cde', end=';', Ext=False) 
		
	@_("closed_statement")
	def statement(self, p):
		return VarDeclaration(name='int', expr='cde', end=';', Ext=False) 
		
	@_("compound_statement")
	def other_statement(self, p):
	#	return p.compound_statement
		pass
	@_("expression_statement")
	def other_statement(self, p):
	#	return p.expression_statement
		pass
	@_("jumpstatement")
	def other_statement(self, p):
	#	return p.jumpstatement
		pass

	@_("WHILE '(' expression ')' open_statement")
	def open_statement(self, p):
	#	return WhileStmt( p.expression, p.open_statement )
		pass
    
	@_("WHILE '(' expression ')' closed_statement")
	def closed_statement(self, p):
	#	return WhileStmt( p.expression, p.closed_statement )
		pass
	@_("IF '(' expression ')' open_statement")
	def open_statement(self, p):
	#	return IfStmt(p.expression, p.open_statement)
		pass
	@_("IF '(' expression ')' other_statement")
	def open_statement(self, p):
	#	return IfStmt(p.expression, p.other_statement)
		pass

	@_("FOR '(' expression_statement expression_statement expression ')' open_statement")
	def open_statement(self, p):
	#	return For( p.expression_statement0, p.expression_statement1, p.expression, p.open_statement )
		pass
	@_("FOR '(' expression_statement expression_statement expression ')' closed_statement")
	def open_statement(self, p):
	#	return For( p.expression_statement0, p.expression_statement1, p.expression, p.closed_statement )
		pass

	@_("other_statement")
	def closed_statement(self, p):
	#	return p.other_statement
		pass      
    
	@_("IF '(' expression ')' closed_statement ELSE open_statement")
	def open_statement(self, p):
	#	return IfStmt(p.expression, p.closed_statement, p.open_statement)
		pass
	@_("IF '(' expression ')' closed_statement ELSE closed_statement")
	def closed_statement(self, p):
	#	return IfStmt(p.expression, p.closed_statement0, p.closed_statement1)
		pass
	@_("statement")
	def statement_list(self, p):
	#	return [p.statement]
		pass

	@_("statement_list statement")
	def statement_list(self, p):
	#	return p.statement_list + [p.statement]
		pass
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