#include <iostream>
#include <vector>
#include <queue>
#include "node.h"
//#include "fluxo.h"

using namespace std;

int main(){
    
    lli n;

    std::cin >> n;

    std::vector<lli> a(n), b(n);

    for (lli i = 0; i < n-1; i++)
    {
        std::cin >> a[i] >> b[i];
    }

    cout << "antes nodes" << endl;

    Nodes nodes = Nodes(a, b, n);

    cout << "antes" << endl;

    nodes.calcula_fluxo();

    cout << "Fluxo em cada vertice do grafo: " << endl;

    for (long long int i = 0; i < n; i++)
    {
        cout << i << ": " << nodes.get_flow_amount(i) << endl;
    }
    
    return 0;
}