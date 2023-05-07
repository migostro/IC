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

std::vector<lli> Node::get_fathers(){
    return fathers;
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
/* Recebe dois vetores out e in, tal que existe um arco que sai de out[i] e vai para in[i], e um intero n (o tamanho dos vetores)
   Inicializa o grafo com esses parametros
*/

/* Private functions */

std::vector<lli> Nodes::random_tree(lli n){
    std::vector<lli> tree(n);

    // defines de atractor
    tree[0] = 0;
    tree[1] = 1;

    for (lli i = 2; i < n; i++)
    {
        // random number in [0,i[
        lli random_num = rand()%i;
        tree[i] = random_num;
    }
    
    return tree;
}

lli Nodes::vector_to_integer(std::vector<int> state_vector){
    lli power = 1, num = 0, n = state_vector.size();

    for (lli i = n_genes-1; i >= 0; i--)
    {
        if (state_vector[i])
            num += power;
        power *= 2;
    }
    
    return num;
}

std::vector<int> Nodes::integer_to_vector(lli num){
    std::vector<int> state_vector(n_genes);
    lli power = node_vector.size()/2;
    for (lli i = 0; i < n_genes; i++){

        if(num/power >= 1){

            state_vector[i] = 1;
            num -= power;
        }
        else{
    
            state_vector[i] = 0;
        }

        power /= 2;
    }
    
    return state_vector;
}

/* Public functions */

/* Creates a random tree with n vertices */
Nodes::Nodes(lli n, lli seed){
    this->n_genes = log2(n);

    node_vector.resize(n);
    srand(seed);
    std::vector<lli> tree = random_tree(n);
    
    for (lli i = 0; i < n; i++)
    {
        node_vector[i].add_adj(tree[i]);
        node_vector[tree[i]].add_father(i);
    }
}

/* Create a pre-defined graph */
Nodes::Nodes(std::vector<lli>& out, std::vector<lli>& in, lli n){
    this->n_genes = log2(n);

    std::vector<Node> novo(n);
    node_vector = novo;
    for (lli i = 0; i < n; i++){
        node_vector[out[i]].add_adj(in[i]);
        node_vector[in[i]].add_father(out[i]);
    }
}

/* 
*/
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

std::vector<lli> Nodes::fathers(lli v){
    return node_vector[v].get_fathers();
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
            node_vector[i].set_weight(node_vector[i].adj_size()-1, 1);
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

std::vector<std::vector<int>> Nodes::infer_regulation_matrix(){
    std::vector<std::vector<int>> actual_states, next_states;
    lli actual, next, n = node_vector.size();

    for (lli i = 0; i < n; i++)
    {
        actual = i;
        next = this->adj(i)[0].second;
        actual_states.push_back(integer_to_vector(actual));
        next_states.push_back(integer_to_vector(next));
    }
    

    return this->M;
}

// define as funções que podem ser usadas no python
PYBIND11_MODULE(nodes, handle) {
    py::class_<Nodes>(handle, "Nodes")
        .def(py::init<lli, lli>())
        .def(py::init<std::vector<lli>&, std::vector<lli>&, lli>())
        .def("add_flow", &Nodes::add_flow)
        .def("add_adj", &Nodes::add_adj)
        .def("set_weight", &Nodes::set_weight)
        .def("adj", &Nodes::adj)
        .def("adj", &Nodes::adj)
        .def("fathers", &Nodes::fathers)
        .def("num_fathers", &Nodes::num_fathers)
        .def("weight", &Nodes::weight)
        .def("get_flow_amount", &Nodes::get_flow_amount)
        .def("calcula_fluxo", &Nodes::calcula_fluxo)
        .def("infer_regulation_matrix", &Nodes::infer_regulation_matrix)
        .def("vector_to_integer", &Nodes::vector_to_integer)
        .def("integer_to_vector", &Nodes::integer_to_vector);
}
