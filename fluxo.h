#ifndef FLUXO_H
#define FLUXO_H

#define lli long long int

class Flow{
    private:
        Nodes * nodes;
        lli n;
    public:
        Flow(lli n, vector<lli> out, vector<lli> in);
        void calcula_fluxo();
}

#endif