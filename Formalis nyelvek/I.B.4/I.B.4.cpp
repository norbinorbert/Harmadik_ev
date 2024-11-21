#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <map>
#include <sstream>
#include <queue>
#include <algorithm>

using namespace std;

int main()
{
    ifstream fin("form_I.B.4.txt");
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

    // edge values not needed
    getline(fin, line);
    vector<string> alphabet;
    ss = stringstream(line);
    while (ss >> token) {
        alphabet.push_back(token);
    }

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
    map<pair<string, string>, vector<string>> graph;
    while (getline(fin, line)) {
        ss = stringstream(line);
        string a, b, c;
        while (ss >> a >> b >> c) {
            graph[make_pair(a, b)].push_back(c);
        }
    }

    map<vector<string>, bool> done;
    queue<vector<string>> q;
    q.push(start_points);
    // map contains: pair<new_source_node, letter> = new_target_node
    map<pair<vector<string>, string>, vector<string>> new_graph;
    vector<vector<string>> end_points2;
    while (!q.empty()) {
        vector<string> node = q.front();
        q.pop();
        if (done[node]) {
            continue;
        }
        done[node] = true;
        for (int i = 0; i < node.size(); i++) {
            if (find(end_points.begin(), end_points.end(), node[i]) != end_points.end()) {
                end_points2.push_back(node);
                break;
            }
        }
        for (string letter : alphabet) {
            vector<string> new_node;
            for (int i = 0; i < node.size(); i++) {
                vector<string> tmp = graph[make_pair(node[i], letter)];
                if (tmp.size() == 0) {
                    continue;
                }
                for (int j = 0; j < tmp.size(); j++) {
                    if (find(new_node.begin(), new_node.end(), tmp[j]) == new_node.end()) {
                        new_node.push_back(tmp[j]);
                    }
                }
            }
            if (new_node.size() == 0) {
                continue;
            }
            sort(new_node.begin(), new_node.end());
            q.push(new_node);
            new_graph[make_pair(node, letter)] = new_node;
        }
    }
    
    // all the new nodes
    vector<string> new_nodes;
    for (auto i = new_graph.begin(); i != new_graph.end(); i++) {
        string node = "\"";
        for (int j = 0; j < i->first.first.size() - 1; j++) {
            node += i->first.first[j] + "-";
        }
        node += i->first.first[i->first.first.size() - 1] + "\""; 
        if (find(new_nodes.begin(), new_nodes.end(), node) == new_nodes.end()) {
            new_nodes.push_back(node);
        }
        node = "\"";
        for (int j = 0; j < i->second.size() - 1; j++) {
            node += i->second[j] + "-";
        }
        node += i->second[i->second.size() - 1] + "\"";
        if (find(new_nodes.begin(), new_nodes.end(), node) == new_nodes.end()) {
            new_nodes.push_back(node);
        }
    }
    for (int i = 0; i < new_nodes.size(); i++) {
        fout << new_nodes[i] << " ";
    }
    fout << endl;

    // alphabet
    for (int i = 0; i < alphabet.size(); i++) {
        fout << alphabet[i] << " ";
    }
    fout << endl;

    // new start point
    fout << "\"";
    for (int i = 0; i < start_points.size() - 1; i++) {
        fout << start_points[i] << "-";
    }
    fout << start_points[start_points.size() - 1] << "\"" << endl;

    // new end points
    for (int i = 0; i < end_points2.size(); i++) {
        fout << "\"";
        for (int j = 0; j < end_points2[i].size() - 1; j++) {
            fout << end_points2[i][j] << "-";
        }
        fout << end_points2[i][end_points2[i].size() - 1] << "\"" << " ";
    }
    fout << endl;

    // edges
    for (auto i = new_graph.begin(); i != new_graph.end(); i++) {
        // start node
        fout << "\"";
        for (int j = 0; j < i->first.first.size() - 1; j++) {
            fout << i->first.first[j] << "-";
        }
        fout << i->first.first[i->first.first.size() - 1] << "\"" << " ";

        // edge value
        fout << i->first.second << " ";

        // end node
        fout << "\"";
        for (int j = 0; j < i->second.size() - 1; j++) {
            fout << i->second[j] << "-";
        }
        fout << i->second[i->second.size() - 1] << "\"" << endl;
    }
}