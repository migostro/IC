#include <iostream>
#include <vector>
#include <queue>
#include "node.h"

using namespace std;

void calcula_fluxo(vector<Node> &nodes, long long int n){
    vector<long long int> accessed(n);
    queue<long long int> queue;
    long long int current, son, flow;

    // encontra e guarda as folhas do grafo
    for (long long int i = 0; i < n; i++)
    {
        if (nodes[i].num_fathers() == 0)
        {
            nodes[i].set_weight(0, 1);
            queue.push(i);
        }
    }

    while (!queue.empty())
    {
        current = queue.front();
        queue.pop();

        while (accessed[current] == nodes[current].num_fathers() && nodes[current].adj_size() > 0)
        {
            son = get<1>(nodes[current].get_adj(0));

            flow = nodes[current].get_flow_amount();

            // adiciona fluxo na aresta que vai de current para son
            nodes[current].set_weight(0, flow);

            // adiciona fluxo no vertice son
            nodes[son].add_flow(flow);

            current = son;
            accessed[current]++;
        }
    }
    // for (long long int i = 0; i < n; i++)
    // {
    //     cout << i << ": " << accessed[i] << endl;
    // }
}

/* Recebe um nó e retorna seu grau
*/
long long int grau(Node node){
    return node.num_fathers()+node.adj_size();
}

double grau_medio(vector<Node> &nodes, long long int n){
    double media = 0;
    for (long long int i = 0; i < n; i++)
    {
        media += grau(nodes[i])/n;
    }
    return media;
}

// double assortatividade(vector<Node> &nodes, vector<pair<long long int, long long int>> &edges, double grau_medio, long long int n){
//     // quantidade de vertices com cada grau
//     vector<long long int> num_grau(n-1, 0), q(n-1);
//     vector<vector<long long int>> e;
//     long long int grau_v;
//     double sigma2 = 0, sum1 = 0, sum2 = 0, r = 0;

//     for (long long int i = 0; i < n-1; i++)
//     {
//         e.push_back(num_grau);
//     }
    
//     cout << "1" << endl;
    


//     for (long long int i = 0; i < n; i++)
//     {
//         grau_v = grau(nodes[i]);
//         num_grau[grau_v]++;
//     }
//     cout << "2" << endl;
//     // constrói q e sigma2
//     for (long long int k = 0; k < n-1; k++)
//     {
//         // calcula q[k]
//         q[k] = k*(num_grau[k]/n)/grau_medio;

//         sum1 += k*k*q[k];
//         sum2 += k*q[k];
//     }
//     cout << "3" << endl;
//     sigma2 = sum1 - sum2*sum2;

//     // construção de e
//     for (auto edge: edges)
//     {
//         e[grau(nodes[edge.first])][grau(nodes[edge.second])]++;
//     }

//     for (long long int i = 0; i < n-1; i++)
//     {
//         for (long long int j = 0; j < n-1; j++)
//         {
//             cout << e[i][i] << ' ';
//         }
//         cout << endl;
//     }

//     cout << "4" << endl;
    
//     for (long long int j = 1; j < n-1; j++)
//     {
//         for (long long int k = 1; k < n-1; k++)
//         {
//             if (num_grau[k] != 0 && num_grau[j] != 0)
//             {
//                 // n-1 é o número de arestas
//                 r += j*k*(e[j][k]/(n-1) - q[j]*q[k]);
//             }
//         }
//         r = r/sigma2;
//     }

//     return r;
// }

int main(){
    
    long long int n, a, b;
    cin >> n;

    vector<Node> nodes(n);
    vector<pair<long long int, long long int>> edges;

    for (long long int i = 0; i < n-1; i++)
    {
        cin >> a >> b;
        nodes[a].add_adj(b);
        nodes[b].add_father(a);
        edges.push_back({a,b});
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
        cout << i << ": " << nodes[i].get_flow_amount() << endl;
    }

    // double r, grau_med = grau_medio(nodes, n);

    // r = assortatividade(nodes, edges, grau_med, n);

    // cout << "r: " << r << endl;
    
    return 0;
}















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