#ifndef NODE_H
#define NODE_H

//#include <vector>
#include <bits/stdc++.h>

using namespace std;

class Node{
    private:
        // quantidade de fluxo que passa pelo vertice
        long long int flow_amount;
        // vetor de pair, onde o peso é o first e o adjacente é o second
        vector<pair<long long int, long long int>> adj;
        vector<long long int> fathers;
    public:
        Node();
        void add_flow(long long int amount);
        void add_adj(long long int v);
        void add_father(long long int v);
        void set_weight(long long int i, long long int weight);
        vector<pair<long long int, long long int>> get_adj();
        pair<long long int, long long int> get_adj(long long int i);
        long long int fathers_size();
        long long int get_weight(long long int i);
        long long int get_flow_amount();
        long long int num_fathers();
        long long int adj_size();
};


// class Nodes{
//     private:
//         vector<Node> node_vector;
//     public:
//         Nodes(long long int n);
//         void add_flow(long long int v, long long int amount);
//         void add_adj(long long int v, long long int u);
//         void set_weight(long long int v, long long int i, long long int weight);
//         vector<pair<long long int, long long int>> adj(long long int v);
//         long long int num_fathers(long long int v);
//         long long int weight(long long int i, long long int j);
//         long long int get_flow_amount(long long int i);
// };


#endif

/*#include <iostream>
#include <vector>
#include <queue>
#include "node.h"

using namespace std;

void calcula_fluxo(Nodes * nodes, long long int n){
    vector<long long int> accessed(n);
    vector<long long int> leaves;
    queue<long long int> queue;
    long long int current, son, flow;

    // encontra e guarda as folhas do grafo
    for (long long int i = 0; i < n; i++)
    {
        if (nodes->num_fathers(i) == 0)
        {
            nodes->set_weight(i, 0, 1);
            leaves.push_back(i);
        }
    }

    for (long long int leaf: leaves)
    {
        queue.push(leaf);
    }

    while (!queue.empty())
    {
        current = queue.front();
        queue.pop();


        while (accessed[current] == nodes->num_fathers(current) && nodes->adj(current).size() > 0)
        {
            son = get<1>(nodes->adj(current)[0]);

            flow = nodes->get_flow_amount(current);

            // adiciona fluxo na aresta que vai de current para son
            nodes->set_weight(current, 0, flow);

            // adiciona fluxo no vertice son
            nodes->add_flow(son, flow);

            current = son;
            accessed[current]++;
        }
        
    }
    // for (long long int i = 0; i < n; i++)
    // {
    //     cout << i << ": " << accessed[i] << endl;
    // }
}

// double assortatividade(Nodes* nodes, long long int n){
//     // quantidade de vertices com cada grau
//     vector<long long int> num_grau(n-1, 0);

//     for (long long int i = 0; i < n; i++)
//     {
        
//     }
    
// }

int main(){
    
    long long int n, a, b;
    cin >> n;

    Nodes * nodes = new Nodes(n);

    for (long long int i = 0; i < n-1; i++)
    {
        cin >> a >> b;
        nodes->add_adj(a, b);
    }

    calcula_fluxo(nodes, n);

    cout << "Fluxo em cada vertice do grafo: " << endl;

    // for (long long int i = 0; i < n; i++)
    // {
    //     if(nodes->adj(i).size() > 0)
    //         cout << nodes->weight(i, 0) << endl;
    // }

    for (long long int i = 0; i < n; i++)
    {
        cout << i << ": " << nodes->get_flow_amount(i) << endl;
    }
    
    return 0;
}*/