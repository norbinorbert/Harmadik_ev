#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <algorithm>
#include <queue>

using namespace std;

void BFS(map<pair<string, string>, string>& graph, vector<string>& nodes, vector<string>& start_points, vector<string>& good_points, vector<string>& good_alphabet) {
    map<string, bool> done;
    for (string point : start_points) {
        done[point] = true;
        queue<string> q;
        q.push(point);
        while (!q.empty()) {
            string curr = q.front();
            done[curr] = true;
            q.pop();
            good_points.push_back(curr);
            for (string node : nodes) {
                if (graph[make_pair(curr, node)].size()) {
                    good_alphabet.push_back(graph[make_pair(curr, node)]);
                    if (!done[node]) {
                        q.push(node);
                    }
                }
            }
        }
    }
}

void I_A_3(ifstream& fin, ofstream& fout) {
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
    ss = stringstream(line);/*
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
    map<pair<string, string>, string> reverse_graph;
    while (getline(fin, line)) {
        ss = stringstream(line);
        string a, b, c;
        while (ss >> a >> b >> c) {
            graph[make_pair(a, c)] = b;
            reverse_graph[make_pair(c, a)] = b;
        }
    }

    // breadth first search for both normal and reverse graph
    vector<string> good_points_from_start, good_alphabet_from_start;
    BFS(graph, nodes, start_points, good_points_from_start, good_alphabet_from_start);
    vector<string> good_points_from_back, good_alphabet_from_back;
    BFS(reverse_graph, nodes, end_points, good_points_from_back, good_alphabet_from_back);

    // points in the final graph
    vector<string> good_points, good_alphabet;
    for (string point : good_points_from_start) {
        if (find(good_points_from_back.begin(), good_points_from_back.end(), point) != good_points_from_back.end()) {
            if (find(good_points.begin(), good_points.end(), point) == good_points.end()) {
                good_points.push_back(point);
            }
        }
    }

    // edge values in the final graph
    for (string edge : good_alphabet_from_start) {
        if (find(good_alphabet_from_back.begin(), good_alphabet_from_back.end(), edge) != good_alphabet_from_back.end()) {
            if (find(good_alphabet.begin(), good_alphabet.end(), edge) == good_alphabet.end()) {
                good_alphabet.push_back(edge);
            }
        }
    }

    // points
    for (int i = 0; i < good_points.size() - 1; i++) {
        fout << good_points[i] << " ";
    }
    fout << good_points[good_points.size() - 1] << endl;

    // edge values
    for (int i = 0; i < good_alphabet.size() - 1; i++) {
        fout << good_alphabet[i] << " ";
    }
    fout << good_alphabet[good_alphabet.size() - 1] << endl;

    // start points
    vector<string> start_points_final;
    for (string tmp : good_points) {
        for (string tmp2 : start_points) {
            if (tmp == tmp2) {
                start_points_final.push_back(tmp);
            }
        }
    }
    for (int i = 0; i < start_points_final.size() - 1; i++) {
        fout << start_points_final[i] << " ";
    }
    fout << start_points_final[start_points_final.size() - 1] << endl;


    // end points
    vector<string> end_points_final;
    for (string tmp : good_points) {
        for (string tmp2 : end_points) {
            if (tmp == tmp2) {
                end_points_final.push_back(tmp);
            }
        }
    }
    for (int i = 0; i < end_points_final.size() - 1; i++) {
        fout << end_points_final[i] << " ";
    }
    fout << end_points_final[end_points_final.size() - 1] << endl;

    // edges
    for (string tmp : good_points) {
        for (string tmp2 : good_points) {
            if (graph[make_pair(tmp, tmp2)].size() != 0) {
                fout << tmp << " " << graph[make_pair(tmp, tmp2)] << " " << tmp2 << endl;
            }
        }
    }
}

int main()
{
    // filter out non-productive and unreachable nodes
    ifstream file1("form_I.B.3.txt");
    ofstream file1_out("parsed_input.txt");
    I_A_3(file1, file1_out);
    file1_out.close();

    ifstream fin("parsed_input.txt");
    ofstream fout("output.txt");
    string line;

    // all nodes
    vector<string> nodes;
    getline(fin, line);
    stringstream ss(line);
    string token;
    while (ss >> token) {
        nodes.push_back(token);
    }

    // edge values
    vector<string> alphabet;
    getline(fin, line);
    ss = stringstream(line);
    while (ss >> token) {
        alphabet.push_back(token);
    }

    // start point
    string start_point;
    getline(fin, start_point);

    // end points
    vector<string> end_points;
    getline(fin, line);
    ss = stringstream(line);
    while (ss >> token) {
        end_points.push_back(token);
    }

    // edges
    map<pair<string, string>, string> graph;
    while (getline(fin, line)) {
        ss = stringstream(line);
        string a, b, c;
        while (ss >> a >> b >> c) {
            graph[make_pair(a, b)] = c;
        }
    }

    // make the automata complete
    bool full = true;
    for (string node : nodes) {
        for (string letter : alphabet) {
            if (graph[make_pair(node, letter)] == "") {
                full = false;
                graph[make_pair(node, letter)] = "END";
            }
        }
    }
    if (!full) {
        nodes.push_back("END");
        for (string letter : alphabet) {
            graph[make_pair("END", letter)] = "END";
        }
    }

    // fill the matrix with * where necessary
    //Jeloljuk meg csillaggal (*) az  ̈osszes (p, q) allapotpart, amelyre p ∈ F es q !∈ F vagy fordıtva
    map<pair<string, string>, string> matrix;
    for (int i = 0; i < nodes.size() - 1; i++) {
        for (int j = i + 1; j < nodes.size(); j++) {
            bool first = find(end_points.begin(), end_points.end(), nodes[i]) != end_points.end();
            bool second = find(end_points.begin(), end_points.end(), nodes[j]) != end_points.end();
            if (first == second) {
                continue;
            }
            matrix[make_pair(nodes[i], nodes[j])] = "*";
            matrix[make_pair(nodes[j], nodes[i])] = "*";
        }
    }

    //Minden jeloletlen (p, q) parhoz rendeljunk egy ures listat
    map<pair<string, string>, vector<pair<string, string>>> list;
    map<pair<string, string>, bool> done;
    for (int i = 0; i < nodes.size() - 1; i++) {
        for (int j = i + 1; j < nodes.size(); j++) {
            //for Minden jeloletlen (p, q) parra
            if (matrix[make_pair(nodes[i], nodes[j])] == "*" || done[make_pair(nodes[i], nodes[j])]) {
                continue;
            }
            queue<pair<string, string>> q;
            q.push(make_pair(nodes[i], nodes[j]));
            while (!q.empty()) {
                pair<string, string> current_pair = q.front();
                pair<string, string> current_pair_reversed = make_pair(current_pair.second, current_pair.first);
                q.pop();
                if (done[current_pair]) {
                    continue;
                }
                done[current_pair] = true;
                vector<pair<string, string>> pairs;
                bool found_star = false;
                // ́es minden a ∈ Σ beture
                for (int k = 0; k < alphabet.size(); k++) {
                    // vizsgaljuk meg a (δ(p, a), δ(q, a)) allapotparokat
                    string first = graph[make_pair(current_pair.first, alphabet[k])];
                    string second = graph[make_pair(current_pair.second, alphabet[k])];
                    if (first == second || found_star) {
                        continue;
                    }
                    pairs.push_back(make_pair(first, second));
                    q.push(make_pair(first, second));
                    //if az igy kapott parok kozul valamelyik meg van csillagozva
                    if (matrix[make_pair(first, second)] == "*") {
                        found_star = true;
                        // csillagozzuk meg a (p, q) part is
                        matrix[current_pair] = "*";
                        matrix[current_pair_reversed] = "*";
                        // a mar elozoleg ehhez a parhoz rendelt lista elemeivel egyutt
                        for (int l = 0; l < list[current_pair].size(); l++) {
                            pair<string, string> tmp = list[current_pair][l];
                            matrix[tmp] = "*";
                        }
                    }
                }
                //else if a fenti allapotparok kozul egy sincs megcsillagozva
                if (!found_star) {
                    //́ırjuk be a (p, q) part a (δ(p, a), δ(q, a)) parokhoz rendelt lista mindegyikebe
                    for (int l = 0; l < pairs.size(); l++) {
                        list[pairs[l]].push_back(current_pair);
                        list[pairs[l]].push_back(current_pair_reversed);
                    }
                }
            }
        }
    }

    // find new nodes by iterating through the matrix
    // if found a spot with no star, iterate through that row from start in case there are other spaces with no stars
    vector<vector<string>> new_nodes;
    map<string, bool> node_done;
    for (int i = 0; i < nodes.size(); i++) {
        if (node_done[nodes[i]]) {
            continue;
        }
        queue<string> q;
        vector<string> new_node;
        q.push(nodes[i]);
        while (!q.empty()) {
            string node = q.front();
            q.pop();
            if (node_done[node]) {
                continue;
            }
            new_node.push_back(node);
            node_done[node] = true;
            for (int j = 0; j < nodes.size(); j++) {
                if (nodes[j] == node) {
                    continue;
                }
                if (matrix[make_pair(node, nodes[j])] != "*") {
                    q.push(nodes[j]);
                }
            }
        }
        new_nodes.push_back(new_node);
    }

    string new_start_node = start_point;
    vector<string> new_end_points;
    map<vector<string>, string> stringified_node;
    for (int i = 0; i < new_nodes.size(); i++) {
        // if new node has length of 1, then it didn't change compared to original graph
        if (new_nodes[i].size() == 1) {
            fout << new_nodes[i][0] << " ";
            stringified_node[new_nodes[i]] = new_nodes[i][0];
            // check if end point
            if (find(end_points.begin(), end_points.end(), new_nodes[i][0]) != end_points.end()) {
                new_end_points.push_back(new_nodes[i][0]);
            }
            continue;
        }
        // node with length bigger than 1 needs to be stringified
        string tmp = "\"";
        bool this_is_the_start_node = false;
        bool this_is_an_end_node = false;
        for (int j = 0; j < new_nodes[i].size() - 1; j++) {
            tmp += new_nodes[i][j] + "-";
            // check if start point
            if (new_nodes[i][j] == start_point) {
                this_is_the_start_node = true;
            }
            // check if end point
            if (find(end_points.begin(), end_points.end(), new_nodes[i][j]) != end_points.end()) {
                this_is_an_end_node = true;
            }
        }
        tmp += new_nodes[i][new_nodes[i].size() - 1] + "\" ";
        stringified_node[new_nodes[i]] = tmp;
        if (this_is_the_start_node) {
            new_start_node = tmp;
        }
        if (this_is_an_end_node) {
            new_end_points.push_back(tmp);
        }
        fout << tmp;
    }
    fout << endl;

    // alphabet
    for (int i = 0; i < alphabet.size(); i++) {
        fout << alphabet[i] << " ";
    }
    fout << endl;

    // start node
    fout << new_start_node << endl;

    // end nodes
    for (int i = 0; i < new_end_points.size(); i++) {
        fout << new_end_points[i] << " ";
    }
    fout << endl;

    // find the new edges
    map<pair<string, string>, string> new_graph;
    for (auto i = graph.begin(); i != graph.end(); i++) {
        string source = i->first.first;
        string letter = i->first.second;
        string destination = i->second;
        int source_index = -1, destination_index = -1;
        for (int j = 0; j < new_nodes.size(); j++) {
            if (find(new_nodes[j].begin(), new_nodes[j].end(), source) != new_nodes[j].end()) {
                source_index = j;
            }
            if (find(new_nodes[j].begin(), new_nodes[j].end(), destination) != new_nodes[j].end()) {
                destination_index = j;
            }
        }
        new_graph[make_pair(stringified_node[new_nodes[source_index]], letter)] = stringified_node[new_nodes[destination_index]];
    }

    // new edges
    for (auto i = new_graph.begin(); i != new_graph.end(); i++) {
        string source = i->first.first;
        string letter = i->first.second;
        string destination = i->second;
        fout << source << " " << letter << " " << destination << endl;
    }
}