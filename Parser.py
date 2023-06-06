import sly
from AST import *
from Lexer import Lexer

class Parser(sly.Parser):
	# debugfile = "minic.txt"

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
		return FuncDeclaration(p.type_specifier,p.declarator,p.compound_statement, lineno=p.lineno)	

	@_("STATIC type_specifier declarator compound_statement")
	def function_definition(self, p):
		return FuncDeclaration(p.type_specifier,p.declarator,p.compound_statement,Static=True, lineno=p.lineno)	

	@_("type_specifier declarator ';'")
	def declaration(self, p):
		return VarDeclaration(p.type_specifier, p.declarator, lineno=p.lineno)
		
	@_("EXTERN type_specifier declarator ';'")
	def declaration(self, p):
		return VarDeclaration(p.type_specifier,p.declarator,Ext=True, lineno=p.lineno)
		
	@_("empty")
	def declaration_list_opt(self, p):
		return []
		
	@_("declaration_list")
	def declaration_list_opt(self, p):
		return p.declaration_list
		
	@_("declaration")
	def declaration_list(self, p):
		return [p.declaration]

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
		return p.declarator
		
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
		return p.parameter_list
		
	@_("parameter_declaration")
	def parameter_list(self, p):
		return [p.parameter_declaration]
		
	@_("parameter_list ',' parameter_declaration")
	def parameter_list(self, p):
		return p.parameter_list+[p.parameter_declaration]
		
	@_("type_specifier declarator")
	def parameter_declaration(self, p):
		return TypeDeclaration(p.type_specifier,p.declarator, p.lineno)
		
	@_("'{' declaration_list_opt statement_list '}'")
	def compound_statement(self, p):
		return p.declaration_list_opt + p.statement_list
		
	# Segun el profesor esta es la que debe ir pero genera
	# WARNING: 19 shift/reduce conflicts
	# @_("'{' statement_list '}'")
	# def compound_statement(self, p):
	# 	return p.statement_list
	
	@_("'{' declaration_list_opt '}'")
	def compound_statement(self, p):
		return p.declaration_list_opt
	
	@_("expression ';'")
	def expression_statement(self, p):
		return p.expression
	
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
		return Binary(p.equality_expression,p[1],p.expression, lineno=p.lineno)
		
	@_("relational_expression")
	def equality_expression(self, p):
		return p.relational_expression
		
	@_("equality_expression EQ relational_expression",
	   "equality_expression NE relational_expression")
	def equality_expression(self, p):
		return Binary(p.equality_expression,p[1],p.relational_expression, lineno=p.lineno)
		
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
		return Binary(p.relational_expression,p[1],p.additive_expression, lineno=p.lineno)
		
	@_("primary_expression")
	def postfix_expression(self, p):
		return p.primary_expression
		
	@_("postfix_expression '(' argument_expression_list ')'")
	def postfix_expression(self, p):
		return Call(p.postfix_expression, p.argument_expression_list)

		
	@_("postfix_expression '(' ')'")
	def postfix_expression(self, p):
		return Call(p.postfix_expression,args=[])
		
	@_("postfix_expression '[' expression ']'")
	def postfix_expression(self, p):
		return Array(p.postfix_expression, p.expression)
		
	@_("expression")
	def argument_expression_list(self, p):
		return [p.expression]
		
	@_("argument_expression_list ',' expression")
	def argument_expression_list(self, p):
		return p.argument_expression_list + [p.expression]
		
	@_("postfix_expression")
	def unary_expression(self, p):
		return p.postfix_expression
		
	@_("'-' unary_expression")
	def unary_expression(self, p):
		return Unary(p[0],p.unary_expression)
		
	@_("'+' unary_expression")
	def unary_expression(self, p):
		return Unary(p[0],p.unary_expression)
		
	@_("'!' unary_expression")
	def unary_expression(self, p):
		return Unary(p[0],p.unary_expression)
		
	@_("'*' unary_expression")
	def unary_expression(self, p):
		return Unary(p[0],p.unary_expression)
		
	@_("'&' unary_expression")
	def unary_expression(self, p):
		return Unary(p[0],p.unary_expression)
		
	@_("unary_expression")
	def mult_expression(self, p):
		return p.unary_expression
		
	@_("mult_expression '*' unary_expression",
	   "mult_expression '/' unary_expression",
	   "mult_expression '%' unary_expression")
	def mult_expression(self, p):
		return Binary(p.mult_expression,p[1],p.unary_expression, lineno=p.lineno)
		
	@_("mult_expression")
	def additive_expression(self, p):
		return p.mult_expression
		
	@_("additive_expression '+' mult_expression",
	   "additive_expression '-' mult_expression")
	def additive_expression(self, p):
		return Binary(p.additive_expression,p[1],p.mult_expression, lineno=p.lineno)
		
	@_("ID")
	def primary_expression(self, p):
		return ID(p[0], p.lineno)
		
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
		return p.expression

	@_("STRING")
	def string_literal(self, p):
		return [p.STRING]

	@_("string_literal STRING")
	def string_literal(self, p):
		return p.string_literal+[p.STRING]

	@_("RETURN ';'")
	def jumpstatement(self, p):
		return Return(lineno=p.lineno)
		
	@_("RETURN expression ';'")
	def jumpstatement(self, p):
		return Return(p.expression, p.lineno)
		
	@_("BREAK ';'")
	def jumpstatement(self, p):
		return Break(p.lineno)
	
	@_("CONTINUE ';'")
	def jumpstatement(self, p):
		return Continue(p.lineno)
	
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
		return p.jumpstatement	

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
	
