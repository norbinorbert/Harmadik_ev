#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <algorithm>

using namespace std;

void backtracking(map<pair<string, string>, string>& graph, string& word, vector<string>& nodes, 
    vector<string>& end_points, string current_node, string current_word, int next_char_index, bool& result) {
    if (result) {
        return;
    }
    if (word == current_word) {
        if (find(end_points.begin(), end_points.end(), current_node) != end_points.end()) {
            result = true;
            return;
        }
    }
    for (string next_node : nodes) {
        string edge_value = graph[make_pair(current_node, next_node)];
        if (next_char_index >= word.size() && edge_value != "eps") {
            return;
        }
        if (edge_value == "eps" || edge_value == string(1, word[next_char_index])) {
            string new_word = current_word;
            int new_next_char_index = next_char_index;
            if(edge_value != "eps"){
                new_word += edge_value;
                new_next_char_index++;
            }
            backtracking(graph, word, nodes, end_points, next_node, new_word, new_next_char_index, result);
        }
    }
}

int main()
{
	ifstream fin("form_I.A.4_2.txt");
    ifstream fin_words("form_I.A.4_2_szavak.txt");
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

    // edge values not needed
    getline(fin, line);
    /*ss = stringstream(line);
    vector<string> alphabet;
    while (ss >> token) {
        alphabet.push_back(token);
    }*/

    // start points
    getline(fin, line);
    ss = stringstream(line);
    vector<string> start_points;
    while (ss >> token) {
        start_points.push_back(token);
    }

    // end points
    getline(fin, line);
    ss = stringstream(line);
    vector<string> end_points;
    while (ss >> token) {
        end_points.push_back(token);
    }

    // edges
    map<pair<string, string>, string> graph;
    while (getline(fin, line)) {
        ss = stringstream(line);
        string a, b, c;
        while (ss >> a >> b >> c) {
            graph[make_pair(a, c)] = b;
        }
    }

    string word;
    while (getline(fin_words, word)) {
        fout << word << " : ";

        bool result = false;
        for (string node : start_points) {
            backtracking(graph, word, nodes, end_points, node, "", 0, result);
        }
        fout << result << endl;
    }

	return 0;
}