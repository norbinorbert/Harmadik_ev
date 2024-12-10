%{
#include "II_3.tab.h"
#include <iostream>
using namespace std;
void update_location();

int column = 1;

#define YY_USER_ACTION update_location();

%}

%option yylineno
%option noyywrap

%%

int {return TYPE_INT;}
double {return TYPE_DOUBLE;}

_+[a-zA-Z]+[0-9]* { yylval.variable = strdup(yytext); return VARIABLE;}

(-?[1-9][0-9]*)|0 { yylval.type = 1; return INT;}
((-?[1-9][0-9]*)|0)\.(0|[0-9]*[1-9]) { yylval.type = 2; return DOUBLE;}
\".*\" {return STRING;}

\+|\-|\*|=|\(|\)|\{|\}|; {return yytext[0];}

write {return WRITE;}
read {return READ;}

if {return IF;}
else {return ELSE;}

while {return WHILE;}

== {return EQUALS;}
!= {return NOT_EQUALS;}

\|\| {return OR;}
&& {return AND;}

\n {column=1;}

\ |\t|\r {}

. {cout << "[" << yylloc.first_line << ", " << yylloc.first_column << "]: lexical error: " << yytext << endl;}

%%

void update_location() {
    yylloc.first_line = yylloc.last_line = yylineno;
    yylloc.first_column = column;
    column += yyleng;
    yylloc.last_column = column;

    for(int i = 0; yytext[i] != '\0'; i++) {
        if(yytext[i] == '\n') {
            yylloc.last_line++;
            yylloc.last_column = 1;
        } else {
            yylloc.last_column++;
        }
    }    
}
