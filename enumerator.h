#ifndef ENUMERATOR_H
#define ENUMERATOR_H
#include "primitiveset.h"

class Enumerator
{
public:

    void init(PrimitiveSet primitiveSet);
    std::vector<std::string> exhaustive_global_search(int n, 
                                                       int max_iters = 0);
    std::vector<std::string> uniform_random_global_search(int n, int num_iters, 
                                                      std::vector<long> seeds);
    std::string uniform_random_global_search_once(int n, long seed = LONG_MAX);
    int calculate_R_i(int i);
    int calculate_S_i(int i);
    int get_Q(int n);
    std::vector<int> calculate_Q(int n);
    std::vector<int> calculate_all_G_i_b(int i);
    int calculate_G_i_b(int i, int b);
    int calculate_l_i_b(int i, int b);
    int calculate_a_i(int i);
    std::string generate_specified_solution(int i, int r, int s, int n);
    std::string ith_n_ary_tree(int i);

    void decimal_to_base_m(int decimal, int m,std::vector<int>& e_base_arity);
    void numberToBase(int n,int b, std::vector<int>& digits);
    int base_m_to_decimal(int v, int m);
    void base_m_to_decimal(const std::vector<int>& v, int m, std::vector<int>& result);
    void base_computations(int e, int m, std::vector<int>& list_bits_deci);
    
private:
    //private class members
    int numVal(char c);
    void deinterleave(std::vector<int> num, int n, std::vector<int>& elemsLin);
    std::vector<std::string> get_element_of_cartesian_product(std::vector<
                                               std::vector<std::string> > pools,
                                               int repeat=1, int index=0);
    int get_arity_of_term(int start_index, const std::string& tree);
    int findOccurenciesCount(const std::string& data, 
                             const std::string& toSearch);

private:
    // Private data members
    PrimitiveSet m_primitiveSet;
    std::vector<int> m_results_for_calculate_Q;
    std::vector<int> m_q;
    std::map<int, std::vector<int> > m_all_g_is;
    std::map<int,int> m_s_is;
    std::map<int,int> m_r_is;
};

#endif // ENUMERATOR_H
