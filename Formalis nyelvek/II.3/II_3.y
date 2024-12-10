/*
    bison -dvt II_3.yacc
    flex II_3.lex
    g++ lex.yy.c II_3.tab.c -o II_3
    II_3.exe <test.txt
*/

%{    
    #include<iostream>
    #include<string>
    #include<cstring>
    #include<map>

    using namespace std;
    
    void yyerror(string);
    extern int yylex();

    map<string, int> variables;

    void addVariable(char* name, int type) {
      string name_str(name); 
      if(variables[name_str] != 0) {
        yyerror("Variable " + name_str + " already declared");
        return;  
      }
      variables[name_str] = type;
    }

    int getVariableType(char* name) {
      string name_str(name);
      if(variables[name_str] == 0){
        yyerror("Variable " + name_str + " not declared yet");
        return 0;
      }
      return variables[name_str];
    }
%}

%union{
  char* variable;
  int type;
}

%token TYPE_INT
%token TYPE_DOUBLE
%token<variable> VARIABLE
%token INT
%token DOUBLE
%token STRING
%token WRITE
%token READ
%token IF
%token ELSE
%token WHILE
%token EQUALS
%token NOT_EQUALS
%token OR
%token AND

%error-verbose
%locations

%start program

%left '+' '-'
%left '*'
%left AND OR

%%

program: instruction ';'
       | instruction error ';'
       | program instruction ';'
       | program instruction error ';'
;

instruction: declaration
           | value_assigning
           | read
           | write
           | if
           | while
           | logical_expression
;

declaration: TYPE_INT VARIABLE {addVariable($2, 1);}
           | TYPE_DOUBLE VARIABLE {addVariable($2, 2);}
;

value_assigning: VARIABLE '=' arithmetic_expression { if (getVariableType($1) != $<type>3) { yyerror("Type mismatch"); } }
;

arithmetic_expression: INT { $<type>$ = 1; }
                     | DOUBLE {$<type>$ = 2; }
                     | VARIABLE {$<type>$ = getVariableType($1)}
                     | arithmetic_expression '+' arithmetic_expression {if ($<type>1 != $<type>3) {yyerror("Type mismatch");} 
                                                                            else {$<type>$ = $<type>1; }; }
                     | arithmetic_expression '-' arithmetic_expression {if ($<type>1 != $<type>3) {yyerror("Type mismatch");} 
                                                                            else {$<type>$ = $<type>1; }; }
                     | arithmetic_expression '*' arithmetic_expression {if ($<type>1 != $<type>3) {yyerror("Type mismatch");} 
                                                                            else {$<type>$ = $<type>1; }; }
                     | '(' arithmetic_expression ')' {$<type>$ = $<type>2; }
                     | '-' arithmetic_expression {$<type>$ = $<type>2; }
;

read: READ VARIABLE
;

write: WRITE arithmetic_expression
     | WRITE STRING
;

logical_expression: arithmetic_expression EQUALS arithmetic_expression {if ($<type>1 != $<type>3) {yyerror("Type mismatch");}}
                  | arithmetic_expression NOT_EQUALS arithmetic_expression {if ($<type>1 != $<type>3) {yyerror("Type mismatch");}}
                  | logical_expression OR logical_expression
                  | logical_expression AND logical_expression
                  | '(' logical_expression ')'
;

if: IF '(' logical_expression ')' '{' program '}'
  | IF '(' logical_expression ')' '{' program '}' ELSE '{' program '}'
;

while: WHILE '(' logical_expression ')' '{' program '}'
;

%%

int main() {
	if (yyparse() == 0) {
      cout << "Done!" << endl;
  }
}

void yyerror(string s) {
  cout << "[" << yylloc.first_line << ", " << yylloc.first_column << "]: " << s << endl;
}
