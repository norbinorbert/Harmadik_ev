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

void read(ifstream& fin, vector<string>& nodes, vector<string>& alphabet, string& start_point, 
    vector<string>& end_points, map<pair<string, string>, string>& graph) {
    string line;

    // all nodes
    getline(fin, line);
    stringstream ss(line);
    string token;
    while (ss >> token) {
        nodes.push_back(token);
    }

    // edge values not needed
    getline(fin, line);
    ss = stringstream(line);
    while (ss >> token) {
        alphabet.push_back(token);
    }

    // start point
    getline(fin, start_point);

    // end points
    getline(fin, line);
    ss = stringstream(line);
    while (ss >> token) {
        end_points.push_back(token);
    }

    // edges
    while (getline(fin, line)) {
        ss = stringstream(line);
        string a, b, c;
        while (ss >> a >> b >> c) {
            graph[make_pair(a, b)] = c;
        }
    }
}

int main()
{
    // filter out non-productive and unreachable nodes
    ifstream file1("form_I.B.1_c1.txt");
    ofstream file1_out("parsed_input1.txt");
    I_A_3(file1, file1_out);
    file1_out.close();
    ifstream file2("form_I.B.1_c2.txt");
    ofstream file2_out("parsed_input2.txt");
    I_A_3(file2, file2_out);
    file2_out.close();

    ifstream fin("parsed_input1.txt");
    ifstream fin2("parsed_input2.txt");

    vector<string> nodes; 
    vector<string> alphabet; 
    string start_point;
    vector<string> end_points; 
    map<pair<string, string>, string> graph;
    read(fin, nodes, alphabet, start_point, end_points, graph);

    vector<string> nodes2;
    vector<string> alphabet2;
    string start_point2;
    vector<string> end_points2;
    map<pair<string, string>, string> graph2;
    read(fin2, nodes2, alphabet2, start_point2, end_points2, graph2);

    // check if alphabets are equivalent
    if (!is_permutation(alphabet.begin(), alphabet.end(), alphabet2.begin(), alphabet2.end())) {
        cout << "Not equivalent" << endl;
        return 0;
    }
    

    // check for each pair if both elements are final states or not
    queue<pair<string, string>> q;
    q.push(make_pair(start_point, start_point2));
    map<pair<string, string>, bool> done;
    while (!q.empty()) {
        pair<string, string> state = q.front();
        q.pop();
        if (done[make_pair(start_point, start_point2)]) {
            continue;
        }
        done[make_pair(start_point, start_point2)] = true;

        // check if one of the elements doesn't exist
        if (state.first == "" || state.second == "") {
            cout << "Not equivalent" << endl;
            return 0;
        }

        // check if both elements are the same state
        bool first_endpoint = false, second_endpoint = false;
        if (find(end_points.begin(), end_points.end(), state.first) != end_points.end()) {
            first_endpoint = true;
        }
        if (find(end_points2.begin(), end_points2.end(), state.second) != end_points2.end()) {
            second_endpoint = true;
        }
        if (first_endpoint != second_endpoint) {
            cout << "Not equivalent" << endl;
            return 0;
        }

        // push new pairs into the queue
        for (string letter : alphabet) {
            pair<string, string> a;
            if (graph[make_pair(state.first, letter)] != "" || graph2[make_pair(state.second, letter)] != "") {
                q.push(make_pair(graph[make_pair(state.first, letter)], graph2[make_pair(state.second, letter)]));
            }
        }
    }
    cout << "Equivalent" << endl;
    return 0;
}