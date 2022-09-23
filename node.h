#ifndef NODE_H
#define NODE_H

//#include <vector>
#include <bits/stdc++.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>


#define lli long long int

class Node{
    private:
        // quantidade de fluxo que passa pelo vertice
        lli flow_amount;
        // vetor de pair, onde o peso é o first e o adjacente é o second
        std::vector<std::pair<lli, lli>> adj;
        std::vector<lli> fathers;
    public:
        Node();
        void add_flow(lli amount);
        void add_adj(lli v);
        void add_father(lli v);
        void set_weight(lli i, lli weight);
        std::vector<std::pair<lli, lli>> get_adj();
        std::pair<lli, lli> get_adj(lli i);
        std::vector<lli> fathers();
        lli fathers_size();
        lli get_weight(lli i);
        lli get_flow_amount();
        lli num_fathers();
        lli adj_size();
};


class Nodes{
    private:
        std::vector<Node> node_vector;
    public:
        Nodes(std::vector<lli>& out, std::vector<lli>& in, lli n);
        void add_flow(lli v, lli amount);
        void add_adj(lli v, lli u);
        void set_weight(lli v, lli i, lli weight);
        std::vector<std::pair<lli, lli>> adj(lli v);
        std::vector<lli> fathers(lli v);
        lli num_fathers(lli v);
        lli weight(lli i, lli j);
        lli get_flow_amount(lli i);
        void calcula_fluxo();
};


#endif
