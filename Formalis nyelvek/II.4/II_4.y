/*
    bison -dvt II_4.y
    flex II_4.lex
    g++ lex.yy.c II_4.tab.c -o II_4
    II_4.exe <test.txt
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

    void addVariable(const char* name, int type) {
      string name_str(name); 
      if(variables[name_str] != 0) {
        yyerror("Variable " + name_str + " already declared");
        return;  
      }
      variables[name_str] = type;
    }

    int getVariableType(const char* name) {
      string name_str(name);
      if(variables[name_str] == 0){
        yyerror("Variable " + name_str + " not declared yet");
        return 0;
      }
      return variables[name_str];
    }

    int level = 0;
    string indentation() {
        string t = "";
        for (int i = 0; i <= level; i++)
            t += "  ";
        return t;
    }

    string KOD;
%}

%union{
  const char* variable;
  const char* value;
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
           | if_else
           | while
;

declaration: TYPE_INT VARIABLE {addVariable($2, 1); KOD += indentation() + "int " + string($<variable>2) + ";\n";}
           | TYPE_DOUBLE VARIABLE {addVariable($2, 2); KOD += indentation() + "double " + string($<variable>2) + ";\n";}
;

value_assigning: VARIABLE '=' {KOD += indentation() + string($<variable>1) + " = ";} arithmetic_expression { if (getVariableType($1) != $<type>4) { yyerror("Type mismatch"); } 
                                                                                              else {KOD += ";\n";}}
;

arithmetic_expression: INT { $<type>$ = 1; KOD += string($<value>1);}
                     | DOUBLE {$<type>$ = 2; KOD += string($<value>1);}
                     | VARIABLE {$<type>$ = getVariableType($1); KOD += string($<variable>1);}
                     | arithmetic_expression '+' {KOD += " + ";} arithmetic_expression {if ($<type>1 != $<type>4) {yyerror("Type mismatch");} 
                                                                            else {$<type>$ = $<type>1; }; }
                     | arithmetic_expression '-' {KOD += " - ";} arithmetic_expression {if ($<type>1 != $<type>4) {yyerror("Type mismatch");} 
                                                                            else {$<type>$ = $<type>1; }; }
                     | arithmetic_expression '*' {KOD += " * ";} arithmetic_expression {if ($<type>1 != $<type>4) {yyerror("Type mismatch");} 
                                                                            else {$<type>$ = $<type>1; }; }
                     | '(' {KOD += "("} arithmetic_expression ')' {KOD += ")"} {$<type>$ = $<type>3; }
                     | '-' {KOD += "-"} arithmetic_expression {$<type>$ = $<type>3; }
;

read: READ VARIABLE {KOD += indentation() + "cin >> " + string($<variable>2) + ";\n";}
;

write: WRITE {KOD += indentation() + "cout << ";} writable_stuff {KOD += ";\n";}
;

writable_stuff: arithmetic_expression
              | STRING { KOD += string($<value>1);}

logical_expression: arithmetic_expression EQUALS {KOD += " == ";} arithmetic_expression {if ($<type>1 != $<type>4) {yyerror("Type mismatch");}}
                  | arithmetic_expression NOT_EQUALS {KOD += " != ";} arithmetic_expression {if ($<type>1 != $<type>4) {yyerror("Type mismatch");}}
                  | arithmetic_expression '>' {KOD += " > ";} arithmetic_expression {if ($<type>1 != $<type>4) {yyerror("Type mismatch");}}
                  | arithmetic_expression '<' {KOD += " < ";} arithmetic_expression {if ($<type>1 != $<type>4) {yyerror("Type mismatch");}}
                  | logical_expression OR {KOD += " || ";} logical_expression
                  | logical_expression AND {KOD += " && ";} logical_expression
;

if: IF '(' {KOD += indentation() + "if ( "; level++;} logical_expression ')' '{' {KOD += "){\n";} program '}' {level-=1; KOD += indentation() + "}\n";}
;

if_else: if ELSE '{' {KOD += indentation() + "else {\n"; level++;} program '}' {level-=1; KOD += indentation() + "}\n";} 

while: WHILE '(' {KOD += indentation() + "while ( "; level++;} logical_expression ')' '{' {KOD += "){\n";} program '}' {level-=1; KOD += indentation() + "}\n";}
;

%%

int main() {
  KOD = "#include <iostream>\nusing namespace std;\n\nint main() {\n";

	yyparse();
  
  KOD = KOD + "}\n";
  cout << KOD << endl;
}

void yyerror(string s) {
  cout << "[" << yylloc.first_line << ", " << yylloc.first_column << "]: " << s << endl;
}
