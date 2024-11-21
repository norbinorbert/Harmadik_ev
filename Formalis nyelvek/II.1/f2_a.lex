/* Keressük meg a bemenetben az egész számokat. A képernyőn csak ezek jelenjenek meg, minden szám új sorban. */

%{
#include <iostream>
using namespace std;
%}

%option noyywrap

%%

([0-9]+) {cout << yytext << endl;}
([0-9]+.[0-9]+) {}
\n {}
. {}

%%

int main() {
    yylex();
}
