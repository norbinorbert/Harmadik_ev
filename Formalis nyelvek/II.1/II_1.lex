/*
    flex II_1.lex
    g++ lex.yy.c -o II_1
    II_1.exe <test.txt
*/
%{
#include <iostream>
using namespace std;

int column = 1;

void poz(string msg){
    cout << "[sor: " << yylineno << ", oszlop: " << column << ", hossz: " << yyleng << "] " << msg << ": " << yytext << endl;
    column += yyleng;
}
%}

%option yylineno
%option noyywrap

%%

int|double {poz("type declaration");}

_+[a-zA-Z]+[0-9]* {poz("variable");}

(-?[1-9][0-9]*)|0 {poz("integer");}
((-?[1-9][0-9]*)|0)\.(0|[0-9]*[1-9]) {poz("fractional number");}
\".*\" {poz("string");}

= {poz("value giving operator");}

\+|\-|\* {poz("arithmetic operator");}
\(|\)|\{|\} {poz("");}

write {poz("write function");}
read {poz("read function");}

if|else {poz("");}

while {poz("");}

== {poz("equals operator");}
!= {poz("not equals operator");}

\|\| {poz("logical or");}
&& {poz("logical and");}

; {poz("instruction end");}

\n {column=1;}
\ |\t {column++;}
. {poz("undefined symbol");}

%%

int main() {
    yylex();
}
