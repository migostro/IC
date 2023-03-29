#include <iostream>
#include <vector>
#include <queue>
#include "node.h"
//#include "fluxo.h"

using namespace std;

int main(){
    
    lli n;

    std::cin >> n;

    // std::vector<lli> a(n), b(n);

    // for (lli i = 0; i < n-1; i++)
    // {
    //     std::cin >> a[i] >> b[i];
    // }

    cout << "antes nodes" << endl;

    // Nodes nodes = Nodes(a, b, n);

    // cout << "antes" << endl;

    // nodes.calcula_fluxo();

    // cout << "Fluxo em cada vertice do grafo: " << endl;

    // for (long long int i = 0; i < n; i++)
    // {
    //     cout << i << ": " << nodes.get_flow_amount(i) << endl;
    // }

    Nodes tree = Nodes(n, 0);

    

    // for (lli i = 0; i < n; i++)
    // {
    //     std::vector<std::pair<lli, lli>> adj = tree.adj(i);
    //     std::cout << "i: " << adj[0].second << ' ';
    // }
    // std::cout << std::endl;
    std::vector<int> vec;

    for (int i = 0; i < n; i++)
    {
        vec = tree.integer_to_vector(i);

        std::cout << tree.vector_to_integer(vec) << ": " << std::endl;
        for(auto v: vec)
            std::cout << v << ' ';
        std::cout << std::endl;

        vec.clear();
    }
    
    
    return 0;
}