#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <algorithm>
#include <stack>

using namespace std;

void backtracking(map<vector<string>, vector<string>>& graph, stack<string>& stack_alphabet, string& word, vector<string>& nodes,
    vector<string>& end_points, string current_node, string current_word, int next_char_index, bool& result) {
    if (result) {
        return;
    }
    if (word == current_word) {
        if ((find(end_points.begin(), end_points.end(), current_node) != end_points.end()) || stack_alphabet.empty()) {
            result = true;
            return;
        }
    }
    if (stack_alphabet.empty()) {
        return;
    }
    for (string next_node : nodes) {
        vector<string> key;
        key.push_back(current_node);
        if (next_char_index < word.length()) {
            key.push_back(string(1, word[next_char_index]));
        }
        else {
            key.push_back("eps");
        }
        key.push_back(next_node);
        vector<string> value = graph[key];
        if (value.size() != 0 && stack_alphabet.top() == value[0] && key[1] != "eps") {
            string new_word = current_word + word[next_char_index];
            int new_next_char_index = next_char_index + 1;
            stack_alphabet.pop();
            for (int i = 1; i < value.size(); i++) {
                if (value[i] != "eps") {
                    stack_alphabet.push(value[i]);
                }
            }
            backtracking(graph, stack_alphabet, word, nodes, end_points, next_node, new_word, new_next_char_index, result);
            for (int i = 1; i < value.size(); i++) {
                if (value[i] != "eps") {
                    stack_alphabet.pop();
                }
            }
            stack_alphabet.push(value[0]);
        }
        else {
            key[1] = "eps";
            value = graph[key];
            if (value.size() == 0 || stack_alphabet.top() != value[0]) {
                continue;
            }
            stack_alphabet.pop();
            for (int i = 1; i < value.size(); i++) {
                if (value[i] != "eps") {
                    stack_alphabet.push(value[i]);
                }
            }
            backtracking(graph, stack_alphabet, word, nodes, end_points, next_node, current_word, next_char_index, result);
            for (int i = 1; i < value.size(); i++) {
                if (value[i] != "eps") {
                    stack_alphabet.pop();
                }
            }
            stack_alphabet.push(value[0]);
        }
    }
}

int main()
{
    ifstream fin("form_I.B.2.txt");
    ifstream fin_words("form_I.B.2_szavak.txt");
    ofstream fout("output.txt");
    string line;

    // all nodes
    getline(fin, line);
    stringstream ss(line);
    string token;
    vector<string> nodes;
    while (ss >> token) {
        nodes.push_back(token);
    }

    // alphabet and stack alphabet not needed
    getline(fin, line);
    getline(fin, line);

    // start point
    getline(fin, line);
    string start_point = line;

    // stack
    stack<string> stack_alphabet;
    getline(fin, line);
    stack_alphabet.push(line);

    // end points
    getline(fin, line);
    ss = stringstream(line);
    vector<string> end_points;
    while (ss >> token) {
        end_points.push_back(token);
    }

    // key will contain: start node, edge value, end node
    // value will contain: stack letter to be removed, stack letters to put in
    map<vector<string>, vector<string>> graph;
    string start, letter, stack_letter;
    while (fin >> start >> letter >> stack_letter) {
        vector<string> key;
        key.push_back(start);
        key.push_back(letter);

        vector<string> value;
        value.push_back(stack_letter);
        getline(fin, line);
        ss = stringstream(line);
        string new_stack_letter;
        while (ss >> new_stack_letter) {
            value.push_back(new_stack_letter);
        }
        key.push_back(value[value.size() - 1]);
        value.pop_back();
        graph[key] = value;
    }
    
    string word;
    while (getline(fin_words, word)) {
        fout << word << " : ";

        bool result = false;
        backtracking(graph, stack_alphabet, word, nodes, end_points, start_point, "", 0, result);
        
        fout << result << endl;
    }

    return 0;
}