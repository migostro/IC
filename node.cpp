#include "node.h"

#include <vector>

using namespace std;

/* NODE */

Node::Node(){
    flow_amount = 1;
}

/* adiciona fluxo que passa pelo vertice 
*/
void Node::add_flow(long long int amount){
    flow_amount += amount;
}

void Node::add_adj(long long int v){
    adj.push_back({0, v});
}

void Node::add_father(long long int v){
    fathers.push_back(v);
}

/* Recebe a posição do vetor adj que será inserido o peso (E NÃO VERTICE) e o peso
*/
void Node::set_weight(long long int i, long long int weight){
    get<0>(adj[i]) = weight;
}

vector<pair<long long int, long long int>> Node::get_adj(){
    return adj;
}

pair<long long int, long long int> Node::get_adj(long long int i){
    return adj[i];
}

long long int Node::fathers_size(){
    return fathers.size();
}

long long int Node::get_weight(long long int i){
    return get<0> (adj[i]);
}

long long int Node::get_flow_amount(){
    return flow_amount;
}

long long int Node::num_fathers(){
    return fathers.size();
}

long long int Node::adj_size(){
    return adj.size();
}

















/* NODES */
// Nodes::Nodes(long long int n){
//     vector<Node> novo(n);
//     node_vector = novo;
// }

// void Nodes::add_flow(long long int v, long long int amount){
//     node_vector[v].add_flow(amount);
// }

// void Nodes::add_adj(long long int v, long long int u){
//     node_vector[v].add_adj(u);
//     node_vector[u].add_father(v);
// }

// /* Recebe um vertice, uma posição do vetor adj (E NÃO VERTICE) que será inserido o peso e o peso
// */
// void Nodes::set_weight(long long int v, long long int i, long long int weight){
//     node_vector[v].set_weight(i, weight);
// }

// vector<pair<long long int, long long int>> Nodes::adj(long long int v){
//     return node_vector[v].get_adj();
// }

// long long int Nodes::num_fathers(long long int v){
//     return node_vector[v].fathers_size();
// }

// long long int Nodes::weight(long long int i, long long int j){
//     return node_vector[i].get_weight(j);
// }

// long long int Nodes::get_flow_amount(long long int i){
//     return node_vector[i].get_flow_amount();
// }



/*


#include <iostream>
#include <vector>
#include <queue>
#include "node.h"

using namespace std;

void calcula_fluxo(vector<Node> nodes, long long int n){
    vector<long long int> accessed(n);
    vector<long long int> leaves;
    queue<long long int> queue;
    long long int current, son, flow;

    // encontra e guarda as folhas do grafo
    for (long long int i = 0; i < n; i++)
    {
        if (nodes[i].num_fathers() == 0)
        {
            cout << "flux 1" << endl;
            cout << i << endl;
            cout << nodes.size() << endl;
            cout << "num adj: " << nodes[i].get_adj().size();
            nodes[i].set_weight(0, 1);
            leaves.push_back(i);
            cout << "flux 2" << endl;
        }
    }

    for (long long int leaf: leaves)
    {
        queue.push(leaf);
    }

    while (!queue.empty())
    {
        cout << "flux 3" << endl;
        current = queue.front();
        queue.pop();


        while (accessed[current] == nodes[current].num_fathers() && nodes[current].get_adj().size() > 0)
        {
            cout << "flux 4" << endl;
            son = get<1>(nodes[current].get_adj()[0]);

            flow = nodes[current].get_flow_amount();

            // adiciona fluxo na aresta que vai de current para son
            nodes[current].set_weight(0, flow);

            // adiciona fluxo no vertice son
            nodes[son].add_flow(flow);

            current = son;
            accessed[current]++;
            cout << "flux 5" << endl;
        }
        cout << "flux 6" << endl;
    }
    // for (long long int i = 0; i < n; i++)
    // {
    //     cout << i << ": " << accessed[i] << endl;
    // }
}

// long long int grau(){

// }

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

    vector<Node> nodes(n);

    for (long long int i = 0; i < n-1; i++)
    {
        cin >> a >> b;
        nodes[a].add_adj(b);
    }

    cout << "passou" << endl;

    calcula_fluxo(nodes, n);

    cout << "Fluxo em cada vertice do grafo: " << endl;

    // for (long long int i = 0; i < n; i++)
    // {
    //     if(nodes->adj(i).size() > 0)
    //         cout << nodes->weight(i, 0) << endl;
    // }

    for (long long int i = 0; i < n; i++)
    {
        cout << i << ": " << nodes[i].get_flow_amount() << endl;
    }
    
    return 0;
}


*/