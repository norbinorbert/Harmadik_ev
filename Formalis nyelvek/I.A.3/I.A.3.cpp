#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include <map>
#include <queue>
#include <algorithm>

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

int main()
{
    ifstream fin("input.txt");
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
            good_points.push_back(point);
        }
    }
    auto it = unique(good_points.begin(), good_points.end());
    good_points.erase(it, good_points.end());
    
    // edge values in the final graph
    for (string edge : good_alphabet_from_start) {
        if (find(good_alphabet_from_back.begin(), good_alphabet_from_back.end(), edge) != good_alphabet_from_back.end()) {
            good_alphabet.push_back(edge);
        }
    }
    it = unique(good_alphabet.begin(), good_alphabet.end());
    good_alphabet.erase(it, good_alphabet.end());

    // points
    for (string tmp : good_points) {
        fout << tmp << " ";
    }
    fout << endl;

    // edge values
    for (string tmp : good_alphabet) {
        fout << tmp << " ";
    }
    fout << endl;

    // start points
    for (string tmp : good_points) {
        for (string tmp2 : start_points) {
            if (tmp == tmp2) {
                fout << tmp << " ";
            }
        }
    }
    fout << endl;


    // end points
    for (string tmp : good_points) {
        for (string tmp2 : end_points) {
            if (tmp == tmp2) {
                fout << tmp << " ";
            }
        }
    }
    fout << endl;

    // edges
    for (string tmp : good_points) {
        for (string tmp2 : good_points) {
            if (graph[make_pair(tmp, tmp2)].size() != 0) {
                fout << tmp << " " << graph[make_pair(tmp, tmp2)] << " " << tmp2 << endl;
            }
        }
    }
    return 0;
}