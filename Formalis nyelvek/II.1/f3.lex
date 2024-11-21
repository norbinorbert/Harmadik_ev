/* Keszítsunk statisztikát a bementi adatokból: sorok száma, karakterek száma, fehér karakterek száma. */

%{
#include <iostream>
using namespace std;
int chars = 0;
int whitespaces = 0;
%}

%option noyywrap
%option yylineno
%%

\ |\t {whitespaces++;}
\n {}
. {chars++;}

%%

int main() {
    yylex();
    cout << chars << " " << whitespaces << " " << yylineno;
}
