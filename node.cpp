// links relevantes para o pybind11
// https://www.youtube.com/watch?v=_5T70cAXDJ0
// https://pybind11.readthedocs.io/en/stable/basics.html
// https://gist.github.com/safijari/f7aec85b89906b4b90a8f33039c11263


// TODO: adicionar no 
// git clone https://github.com/pybind/pybind11.git


#include "node.h"

namespace py = pybind11;

using namespace std;

/* NODE */

Node::Node(){
    flow_amount = 1;
}

/* adiciona fluxo que passa pelo vertice 
*/
void Node::add_flow(lli amount){
    flow_amount += amount;
}

void Node::add_adj(lli v){
    adj.push_back({0, v});
}

void Node::add_father(lli v){
    fathers.push_back(v);
}

/* Recebe a posição do vetor adj que será inserido o peso (E NÃO VERTICE) e o peso
*/
void Node::set_weight(lli i, lli weight){
    get<0>(adj[i]) = weight;
}

std::vector<std::pair<lli, lli>> Node::get_adj(){
    return adj;
}

std::pair<lli, lli> Node::get_adj(lli i){
    return adj[i];
}

lli Node::fathers_size(){
    return fathers.size();
}

lli Node::get_weight(lli i){
    return get<0>(adj[i]);
}

lli Node::get_flow_amount(){
    return flow_amount;
}

lli Node::num_fathers(){
    return fathers.size();
}

lli Node::adj_size(){
    return adj.size();
}


/*************************************** NODES ****************************************/
Nodes::Nodes(std::vector<lli>& out, std::vector<lli>& in, lli n){
    std::vector<Node> novo(n);
    node_vector = novo;
    for (lli i = 0; i < n-1; i++){
        node_vector[out[i]].add_adj(in[i]);
        node_vector[in[i]].add_father(out[i]);
    }
}

void Nodes::add_flow(lli v, lli amount){
    node_vector[v].add_flow(amount);
}

void Nodes::add_adj(lli v, lli u){
    node_vector[v].add_adj(u);
    node_vector[u].add_father(v);
}

/* Recebe um vertice, uma posição do vetor adj (E NÃO VERTICE) que será inserido o peso e o peso
*/
void Nodes::set_weight(lli v, lli i, lli weight){
    node_vector[v].set_weight(i, weight);
}

std::vector<std::pair<lli, lli>> Nodes::adj(lli v){
    return node_vector[v].get_adj();
}

lli Nodes::num_fathers(lli v){
    return node_vector[v].fathers_size();
}

lli Nodes::weight(lli i, lli j){
    return node_vector[i].get_weight(j);
}

lli Nodes::get_flow_amount(lli i){
    return node_vector[i].get_flow_amount();
}

void Nodes::calcula_fluxo(){
    lli n = node_vector.size();
    std::vector<lli> accessed(n);
    std::queue<lli> queue;
    lli current, son, flow;

    // encontra e guarda as folhas do grafo
    for (lli i = 0; i < n; i++)
    {
        if (node_vector[i].num_fathers() == 0)
        {
            node_vector[i].set_weight(0, 1);
            queue.push(i);
        }
    }

    while (!queue.empty())
    {
        current = queue.front();
        queue.pop();

        while (accessed[current] == node_vector[current].num_fathers() && node_vector[current].adj_size() > 0)
        {
            son = get<1>(node_vector[current].get_adj()[0]);

            flow = node_vector[current].get_flow_amount();

            // adiciona fluxo na aresta que vai de current para son
            node_vector[current].set_weight(0, flow);

            // adiciona fluxo no vertice son
            node_vector[son].add_flow(flow);

            current = son;
            accessed[current]++;
        }
    }
}

// define as funções que podem ser usadas no python
PYBIND11_MODULE(nodes, handle) {
    py::class_<Nodes>(handle, "Nodes")
        .def(py::init<std::vector<lli>&, std::vector<lli>&, lli>())
        .def("add_flow", &Nodes::add_flow)
        .def("add_adj", &Nodes::add_adj)
        .def("set_weight", &Nodes::set_weight)
        .def("adj", &Nodes::adj)
        .def("num_fathers", &Nodes::num_fathers)
        .def("weight", &Nodes::weight)
        .def("get_flow_amount", &Nodes::get_flow_amount)
        .def("calcula_fluxo", &Nodes::calcula_fluxo);
}
