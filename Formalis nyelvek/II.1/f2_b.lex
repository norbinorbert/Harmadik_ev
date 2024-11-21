/* Írassuk ki a valós szamokat, illetve kezeljuk le az előjeleket is. */

%{
#include <iostream>
using namespace std;
%}

%option noyywrap

%%

(-?[1-9][0-9]*)|0 {cout << yytext << endl;}
((-?[1-9][0-9]*)|0)\.(0|[0-9]*[1-9]) {cout << yytext << endl;}
\n {}
. {}

%%

int main() {
    yylex();
}
