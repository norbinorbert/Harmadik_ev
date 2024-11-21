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
    int line_number = 1;
    while (getline(fin, line)) {
        if (line_number == 1) {
            fout << line << " END" << endl;
        }
        else if (line_number == 2) {
            fout << line << endl;
        }
        else if (line_number == 3) {
            fout << line << endl << "END" << endl;
        }
        else {
            stringstream ss(line);
            string token;
            int number_of_tokens = 0;
            while (ss >> token) {
                number_of_tokens++;
            }

            if (number_of_tokens == 2) {
                fout << line << " END" << endl;
            }
            else {
                fout << line << endl;
            }
        }
        line_number++;
    }

    return 0;
}