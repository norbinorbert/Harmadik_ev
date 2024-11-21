#include <iostream>
#include <fstream>
#include <string>
#include <sstream>

using namespace std;

int main()
{
    ifstream fin("input.txt");
    ofstream fout("output.txt");
    string line;

    string dot_code = "digraph G{\nrankstep = 0.5;\n\
nodestep=0.5;\n\
rankdir=LR;\n\
node [shape=\"circle\",fontsize=\"16\"];\n\
fontsize=\"10\";\n\
compound=true;\n\n";

    getline(fin, line);
    getline(fin, line);

    getline(fin, line);
    stringstream ss(line);
    string token;
    int counter = 0;
    while (ss >> token) {
        dot_code += "start" + to_string(counter) + " [shape = point, style = invis]; \n";
        dot_code += "start" + to_string(counter) + "->" + token + "\n";
        counter++;
    }

    getline(fin, line);
    ss = stringstream(line);
    while (ss >> token) {
        dot_code += token + " [shape=doublecircle];\n";
    }

    while (getline(fin, line)) {
        ss = stringstream(line);
        string a, b, c;
        ss >> a >> b >> c;
        dot_code += a + "->" + c + " [label=" + b + "];\n";
    }

    dot_code += "}";
    fout << dot_code;
    return 0;
}