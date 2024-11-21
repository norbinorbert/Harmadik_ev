/* Alakítsuk a kis "a" betűket nagy "A" betűkké. */

%{
#include <iostream>
using namespace std;
%}

%option noyywrap

%%

a {cout << "A";}

%%

int main() {
    yylex();
}
