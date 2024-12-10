/*
    bison -dvt II_2.y
    flex II_2.lex
    g++ lex.yy.c II_2.tab.c -o II_2
    II_2.exe <test.txt
*/

%{    
    #include<iostream>
    using namespace std;
    void yyerror(const char*);
    extern int yylex();
%}

%token TYPE_INT
%token TYPE_DOUBLE
%token VARIABLE
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
           | arithmetic_expression
           | read
           | write
           | if
           | while
           | logical_expression
;

declaration: TYPE_INT VARIABLE
           | TYPE_DOUBLE VARIABLE
;

value_assigning: VARIABLE '=' arithmetic_expression
;

arithmetic_expression: INT
                     | DOUBLE
                     | VARIABLE
                     | arithmetic_expression '+' arithmetic_expression
                     | arithmetic_expression '-' arithmetic_expression
                     | arithmetic_expression '*' arithmetic_expression
                     | '(' arithmetic_expression ')'
                     | '-' arithmetic_expression
;

read: READ VARIABLE
;

write: WRITE arithmetic_expression
     | WRITE STRING
;

logical_expression: arithmetic_expression EQUALS arithmetic_expression
                  | arithmetic_expression NOT_EQUALS arithmetic_expression
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

void yyerror(const char* s) {
  cout << "[" << yylloc.first_line << ", " << yylloc.first_column << "]: " << s << endl;
}