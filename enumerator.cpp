/*

The implementation of the global optimization by uniform random global search
(GOURGS) enumerator class in C++.

Authors: Razvan Tarnovan, Sohrab Towfighi 
Copyright: Sohrab Towfighi 2020

*/

#include <time.h>
#include <stdio.h>
#include <string>
#include <random>
#include <chrono>
#include "enumerator.h"
#include "boost/algorithm/string/replace.hpp"
#include "boost/random/discrete_distribution.hpp"
#include <sstream>

namespace patch
{
// This to_string was only implemented to bypass a bug in gcc
    template < typename T > std::string to_string(const T& n)
    {
        std::ostringstream stm ;
        stm << n ;
        return stm.str() ;
    }
}

using namespace std;
using namespace std::chrono;
namespace mp = boost::multiprecision;


void Enumerator::init(PrimitiveSet primitiveSet)
{
    m_primitiveSet = primitiveSet;
}

std::vector<std::string> Enumerator::exhaustive_global_search(int n, 
                                                              int max_iters)
{
    /* 
    Produces a list of candidate solutions by incrementally increasing the 
    operator/terminals configurations indices (r, and s). When these values
    are maxed out for a given tree index, the tree index is incremented.
    
    Parameters
    ----------

    n: int 
        User specified number of permitted trees. As n increases, the search 
        space becomes larger and trees become more complex.
    
    max_iters: int
        The maximum number of solutions which can be considered. If set to zero,
        the search will consider all possible solutions up to and including a 
        tree of complexity `i == n`. 
        
    Returns 
    -------
    candidate_solutions: std::vector<std::string>
        A vector of strings, with each string being a candidate solution. 
    */
    int iters = 1;
    vector<string> candidate_solutions;
    for(int i = 0; i < n; i++)
    {
        int R_i = calculate_R_i(i);
        int S_i = calculate_S_i(i);
        for(int r=0; r < R_i; r++)
        {
            for(int s=0; s < S_i; s++)
            {
                candidate_solutions.push_back(generate_specified_solution(i, 
                                                                    r, s, n));
                if(max_iters > 0 &&  iters++ >= max_iters)
                {
                    return candidate_solutions;
                }
            }
        }
    }
    return candidate_solutions;
}

std::vector<std::string> Enumerator::uniform_random_global_search(int n, 
                                                                  int num_iters, 
                                                        std::vector<long> seeds)
{
    /* 
    Produces a list of candidate solutions by randomly sampling from the set of
    operator/terminals configurations indices (r_i, and s_i), ensuring that the 
    probably of selecting a given tree `i` in `{0,...,n}` is proportional to 
    the number of possible equations in the `i^{th}` tree.
    
    Parameters
    ----------

    n: int 
        User specified number of permitted trees. As n increases, the search 
        space becomes larger and trees become more complex.
    
    num_iters: int
        The number of solutions which will be considered. 
        
    seeds: std::vector<long>
        Every time we run uniform_random_global_search_once, we supply it a 
        different random seed. This implementation was deemed necessary because 
        during multiprocessing runs, different processes were being given the 
        same seed, and so were producing identical output.
        
    Returns 
    -------
    solutions: std::vector<std::string>
        A vector of strings, with each string being a candidate solution. 
    */
    vector<string> solutions;
    if(seeds.size() > 0 && num_iters != seeds.size())
    {
        cerr << "Enumerator::uniform_random_global_search: invalid seeds number" 
                                                                        << endl;
        return solutions;
    }
    for(int i=0;i<num_iters;i++)
    {
        if(seeds.size() > 0)
            solutions.push_back(uniform_random_global_search_once(n, seeds[i]));
        else
            solutions.push_back(uniform_random_global_search_once(n));
    }
    return solutions;
}

string Enumerator::uniform_random_global_search_once(int n, long seed)
{
    vector<int> weights = calculate_Q(n);
    double sum_of_weight = 0;
    for(int j=0; j<n; j++) {
       sum_of_weight += weights[j];
    }
    vector<double> norm_weights;
    for(int j=0; j<n; j++) {
       norm_weights.push_back(weights[j] / sum_of_weight);
    }

    boost::mt19937 gen;
    if( seed != LONG_MAX )
    {
        gen.seed(seed);
    }
    if( seed == LONG_MAX)
    {
        auto duration = std::chrono::system_clock::now().time_since_epoch();
        auto nanos = std::chrono::duration_cast<std::chrono::nanoseconds>(
                                                              duration).count();
        gen.seed(nanos);
    }

    boost::random::discrete_distribution<> weightdist(norm_weights.begin(), 
                                                            norm_weights.end());
    int i = weightdist(gen);
    int r_i = calculate_R_i(i);
    int s_i = calculate_S_i(i);
    boost::random::uniform_int_distribution<> r_dist(0, r_i - 1);
    boost::random::uniform_int_distribution<> s_dist(0, s_i - 1);
    int r = r_dist(gen);
    int s = s_dist(gen);
    //    int i = 918;
    // int r = 27; int s = 31625;
    //printf("\ni: %d, r: %d, s: %d, n: %d\n",i,r,s,n);
    string candidate_solution = generate_specified_solution(i, r, s, n);
    return candidate_solution;
}

int Enumerator::calculate_R_i(int i)
{
    std::map<int, int>::iterator it = m_r_is.find(i);
    if(it != m_r_is.end())
    {
        return it->second;
    }
    if (i == 0)
    {
        return 1;
    }
    int r_i = 1;
    vector<int> all_G_i_b = calculate_all_G_i_b(i);
    for(int ii = 0; ii < all_G_i_b.size(); ii++)
    {
        int g_i_b = all_G_i_b[ii];
        if(g_i_b != 0)
        {
            r_i = r_i * g_i_b;
        }
    }
    m_r_is[i] = r_i;
    return r_i;
}

int Enumerator::calculate_S_i(int i)
{
    std::map<int, int>::iterator it = m_s_is.find(i);
    if(it != m_s_is.end())
    {
        return it->second;
    }
    int m = m_primitiveSet.get_terminals().size();
    int j_i = calculate_a_i(i);
    //TODO: remove usage of mempower and use pow instead, m and j_i have 
    // small values
    int s_i = pow(m, j_i);
    m_s_is[i] = s_i;
    return s_i;
}

int Enumerator::get_Q(int n)
{
    if(n > 1)
    {
        if( m_q.size() < n)
        {
            vector<int> res = calculate_Q(n);
        }
        return m_q[n-1];
    }
    return 0;
}

vector<int> Enumerator::calculate_Q(int n)
{
    int q = 0;
    int r_i;
    int s_i;
    int product;
    if(n < m_results_for_calculate_Q.size())
    {
        return m_results_for_calculate_Q;
    }
    for(int i=0;i<n;i++)
    {
        r_i = calculate_R_i(i);
        s_i = calculate_S_i(i);
        product = s_i * r_i;
        q+=product;
        m_q.push_back(q);
        m_results_for_calculate_Q.push_back(product);

    }
    return m_results_for_calculate_Q;
}

vector<int> Enumerator::calculate_all_G_i_b(int i)
{
    std::map<int, std::vector<int> >::iterator it = m_all_g_is.find(i);
    if(it != m_all_g_is.end())
    {
        return it->second;
    }
    vector<int> arities = m_primitiveSet.get_arities();
    int k = arities.size();
    vector<int> list_g_i_b;
    for(int b=0; b < k;b++)
    {
        list_g_i_b.push_back(calculate_G_i_b(i,b));
    }
    m_all_g_is[i] = list_g_i_b;
    return list_g_i_b;
}

int Enumerator::calculate_G_i_b(int i, int b)
{
    vector<int> arities = m_primitiveSet.get_arities();
    int f_b = m_primitiveSet.get_operators(arities[b]).size();
    int l_i_b = calculate_l_i_b(i, b);
    int g_i_b = pow(f_b, l_i_b);
    return g_i_b;
}

int Enumerator::calculate_l_i_b(int i, int b)
{
    vector<int> arities = m_primitiveSet.get_arities();
    int k = arities.size();
    int l_i_b;
    if(i == 0)
    {
        l_i_b = 0;
    }
    else if (1 <= i && i <= k)
    {
        if(b == i - 1)
        {
            l_i_b = 1;
        }
        else
        {
            l_i_b = 0;
        }
    }
    else
    {
        l_i_b = 0;
        int e = (i - 1) / k;
        int j = (i - 1) % k;
        int m = arities[j];
        if (m == arities[b])
        {
            l_i_b += 1;
        }
        if( m == 1 )
        {
            l_i_b += calculate_l_i_b(e,b);
        }
        else if( m > 1)
        {
            vector<int> list_bits_deci;
            base_computations(e,m,list_bits_deci);
            for(int ii = 0; ii < list_bits_deci.size(); ii++)
            {
                int i_deinterleave = list_bits_deci[ii];
                l_i_b += calculate_l_i_b(i_deinterleave, b);
            }
        }
        else
        {
        	cerr << "Enumerator::calculate_l_i_b: Invalid value for m" << endl;
        	throw 2;
        }
    }
    return l_i_b;
}

int Enumerator::calculate_a_i(int i)
{
    vector<int> arities = m_primitiveSet.get_arities();
    int k = arities.size();
    int a_i = 0;
    if(i == 0)
    {
        a_i = 1;
    }
    else if (1 <= i && i <= k)
    {
        a_i = arities[i-1];
    }
    else
    {
        int e = (i - 1) / k;
        int j = (i - 1) % k;
        int m = arities[j];
        if( m == 1 )
        {
            a_i += calculate_a_i(e);
        }
        else if ( m > 1)
        {
            vector<int> list_bits_deci;
            base_computations(e,m,list_bits_deci);
            for(int ii = 0; ii < list_bits_deci.size(); ii++)
            {
                int i_deinterleave = list_bits_deci[ii];
                a_i += calculate_a_i(i_deinterleave);
            }
        }
        else
        {
        	cerr << "Enumerator::calculate_a_i: Invalid value for m" << endl;
        	throw 2;
        }
    }
    return a_i;
}

string Enumerator::generate_specified_solution(int i, int r, int s, int n)
{
    string msg;
    int r_i = calculate_R_i(i);
    int s_i = calculate_S_i(i);
    if ((r >= r_i) || (r < 0))
    {
        msg = "Enumerator::generate_specified_solution: invalid operator";
        cerr << msg << endl;
        throw 2;
    }
    if((s >= s_i)  || (s < 0))
    {
        msg = "Enumerator::generate_specified_solution InvalidTreeIndex" ; 
        cerr << msg << endl;
        throw 2;
    }
    if (i > n)
    {
        msg = "Enumerator::generate_specified_solution InvalidTreeIndex i>n";
        cerr << msg << endl;
        throw 2;
    }
    string tree = "";
    tree = ith_n_ary_tree(i);
    vector<int> g_i_b_values = calculate_all_G_i_b(i);
    vector<int> operator_config_indices;

    //equivalent of python unravel_index (value, list)
    operator_config_indices.push_back(r);
    for(int ii = 1; ii < g_i_b_values.size(); ii++)
    {
        operator_config_indices.push_back(0);
    }

    vector<vector<string>> operator_config;
    vector<int> arities = m_primitiveSet.get_arities();
    for(int b = 0; b < operator_config_indices.size(); b++)
    {
        int z = operator_config_indices[b];
        int arity = arities[b];
        int l_i_b = calculate_l_i_b(i, b);
        vector<vector<string> > operators;
        operators.push_back(m_primitiveSet.get_operators(arity));
        vector<string> config = get_element_of_cartesian_product(operators, 
                                                                     l_i_b, z);
        operator_config.push_back(config);
    }
    int a_i = calculate_a_i(i);
    vector<vector<string>> terminals;
    terminals.push_back(m_primitiveSet.get_terminals());
    vector<string> terminal_config = get_element_of_cartesian_product(terminals, 
                                                                        a_i, s);

    string workingTree = tree;
    string tempTree;
    int num_opers = std::count(tree.begin(), tree.end(), '[');
    int start_index = -1;
    for(int ii = 0; ii < num_opers ; ii++)
    {
        start_index = workingTree.find("[", start_index+1);
        int arity = get_arity_of_term(start_index, workingTree);
        int index = -1;
        for(int jj = 0; jj < arities.size(); jj++)
        {
            if(arities[jj] == arity)
            {
                index = jj;
                break;
            }
        }
        if(index == -1)
        {
            continue;
        }
        vector<string> operator_config_vector = operator_config[index];
        string my_operator = operator_config_vector[
                                               operator_config_vector.size()-1];
        operator_config[index].pop_back();
        tempTree = workingTree.substr(0, start_index);
        tempTree.append(my_operator); tempTree.append("("); 
        tempTree.append(workingTree.substr(start_index+1, 
                                      workingTree.length() - start_index - 1));
        workingTree = tempTree;
        start_index += my_operator.size();
    }
    boost::replace_all(workingTree, "]", ")");
    int num_terminals = findOccurenciesCount(workingTree, "..");
    if (num_terminals != terminal_config.size())
    {
        cerr << "Count of '..' must equal length of terminal_config vector" 
                                                                        << endl;
        throw 2;
    }
    for(int ii = 0; ii < num_terminals; ii++)
    {
        string terminal = terminal_config[terminal_config.size()-1];
        terminal_config.pop_back();
        boost::replace_first(workingTree, "..", terminal);
    }
    tree = workingTree;
    return tree;
}

string Enumerator::ith_n_ary_tree(int i)
{
    vector<int> arities = m_primitiveSet.get_arities();
    string tree ="";
    int k = arities.size();
    if(i == 0)
    {
        tree = "..";
    }
    else if (1 <=i && i <= k)
    {
        tree = "[";
        int m = arities[i-1];
        for(int j=0; j<m; j++)
        {
            tree +="..,";
        }
        string cutTree = tree.substr(0, tree.size() - 1);
        tree = cutTree + "]";
    }
    else
    {
        int e = (i - 1) / k;
        int j = (i - 1) % k;
        int m = arities[j];
        vector<string> subtrees;
        if( m == 1 )
        {
            subtrees.push_back( ith_n_ary_tree( e ) );
        }
        else if ( m > 1 )
        {
            vector<int> list_bits_deci;
            base_computations(e,m,list_bits_deci);
            for(int ii = 0; ii < list_bits_deci.size(); ii++)
            {
                int i_deinterleave = list_bits_deci[ii];
                subtrees.push_back(ith_n_ary_tree(i_deinterleave));
            }
        }
        tree = "[";
        //tree.append(",");
        for(int j = 0; j < subtrees.size(); j++)
        {
            tree.append(subtrees[j]);
            if(j < subtrees.size() - 1)
            {
               tree.append(",");
            }
        }
        tree.append("]");
    }
    return tree;
}

int Enumerator::get_arity_of_term(int start_index, const string& tree){
    /*
    Returns the arity of the operator which can be placed at index
    `start_index` within the tree
    Parameters
    ----------
    start_index: int
        Index at which the operator is set to begin. Needs to match to a square
        bracket within the `pyGOURGS` generated string tree
    tree: string
        The solution tree as generated by `pyGOURGS`
    Returns
    -------
    arity: the arity of the operator at `start_index` in `tree`
    */
    int bracket_counter = 0;
    int arity = 1;
    if (tree.c_str()[start_index] != '[')
    {
        cerr << "Start index must point to a square bracket";
        throw 2;
    }
    int len_solution = tree.length();
    for (int i=start_index; i<len_solution; i++)
    {
        if (tree.c_str()[i] == '[')
        {
            bracket_counter = bracket_counter + 1;
        }
        else if (tree.c_str()[i] == ']')
        {
            bracket_counter = bracket_counter - 1;
        }
        if ((tree.c_str()[i] == ',') && (bracket_counter == 1))
        {
            arity = arity + 1;
        }
        if (bracket_counter == 0)
        {
            break;
        }
    }
    return arity;
}

void Enumerator::decimal_to_base_m(int v, int m, vector<int>& e_base_arity)
{
    if(v < 0)
    {
        cerr << "decimal_to_base_m: Do not supply negative values" << endl;
        throw 2;
    }
    if (v == 0)
    {
        e_base_arity.push_back(0);
    }
    else
    {
        if (m == 1)
        {
            e_base_arity.clear();
            e_base_arity.reserve( v - 1);
            for(int i = 0; i < v; i++)
            {
                e_base_arity.push_back(1);
            }
        }
        else if(m >= 2)
        {
            numberToBase(v, m,e_base_arity);
        }
        else
        {
            cerr << " Enumerator::decimal_to_base_m: Invalid m" << endl;
            throw 2;
        }
    }
}

void Enumerator::numberToBase(int n, int b, vector<int>& digits)
{
    digits.clear();
    if (n == 0)
    {
        digits.push_back(0);
        return;
    }
    while (n != 0)
    {
        digits.push_back(n % b);
        n /= b;
    }
     std::reverse(digits.begin(), digits.end());
}

int Enumerator::base_m_to_decimal(int v, int m)
{
    int result = 0;
    if( m > 10 )
    {
        cerr << "Enumerator::base_m_to_decimal: Cannot handle m > 10 and type(v) is int. Input v as list";
        throw 2;
    }
    else if( m == 1 )
    {
        string vstring = to_string(v);
        for(int i = 0; i < vstring.size(); i++)
        {
            result += numVal(vstring[i]);
        }
    }
    else if ( m >= 2 )
    {
       vector<int> number;
       int power = 1;
       string vstring = to_string(v);
       for(int i = 0; i < vstring.size(); i++)
       {
           number.push_back( numVal(vstring[i] ) );
       }
       for(int i = number.size() - 1; i >= 0; i--)
       {
          // A digit in input number must be
          // less than number's base
          if ( number[i] > m )
          {
             printf("Invalid Number");
             return -1;
          }

          result += number[i] * power;
          power *= m;
       }
    }
    return result;
}

void Enumerator::base_m_to_decimal(const std::vector<int>& v, int m, vector<int>& list_bits_deci)
{
    list_bits_deci.clear();
    list_bits_deci.reserve(v.size());
    for(vector<int>::const_iterator it = v.begin(); it != v.end(); it++)
    {
        list_bits_deci.push_back(base_m_to_decimal(*it,m));
    }
}

void Enumerator::base_computations(int e, int m, std::vector<int>& list_bits_deci)
{
    vector<int> e_base_arity;
    decimal_to_base_m(e,m,e_base_arity);
    vector<int> list_bits;
    deinterleave(e_base_arity, m,list_bits);
    base_m_to_decimal(list_bits, m, list_bits_deci);
}

int Enumerator::numVal(char c)
{
    if (c >= '0' && c <= '9')
        return (int)c - '0';
    else
        return (int)c - 'A' + 10;
}

void Enumerator::deinterleave(vector<int> num, int m, vector<int>& elemsLin)
{
    vector<vector<int> > elements;
    for(int i = 0; i < m; i++)
    {
        vector<int> empty;
        elements.push_back(empty);
    }
    while((num.size() % m) != 0)
    {
        num.insert(num.begin(), 0);
    }
    for(int i = 0; i < num.size() ; i+=m)
    {
        for(int j = 0; j < m; j++)
        {
            elements[j].push_back(num[i+j]);
        }
    }
    elemsLin.clear();
    elemsLin.reserve(elements.size());
    for(int i = 0; i < elements.size();i++)
    {
       elemsLin.push_back(0);
       for(int j=0; j < elements[i].size(); j++)
       {
           elemsLin[i] += elements[i][j] * (pow(10,elements[i].size() - j - 1));
       }
    }
}
vector<string> Enumerator::get_element_of_cartesian_product(
                                                vector<vector<string> > pools,
                                                int repeat,
                                                int index)
{
    vector<vector<string> > pools_temp;
    vector<string> ith_item;

    if(repeat == 0 || pools.size() == 0)
    {
        return ith_item;
    }

    for (int i=0; i<repeat; i++)
    {
        pools_temp.push_back(pools[0]);
    }
    int len_product = pools_temp[0].size();
    int len_pools = pools_temp.size();
    for (int j=1; j<len_pools; j++)
    {
        len_product *= pools_temp[j].size();
    }
    if (index >= len_product)
    {
        cerr << "index + 1 is bigger than the length of the product";
        throw 2;
    }
    vector<int> index_list;
    int denominator = 1;
    int ith_pool_index = 0;
    for (int j=0; j<len_pools; j++)
    {
        ith_pool_index = index;
        denominator = 1;
        for (int k=j+1; k<len_pools; k++)
            {denominator *= pools_temp[k].size();}
        ith_pool_index /= denominator;
        if (j != 0)
            {ith_pool_index %= pools_temp[j].size();}
        index_list.push_back(ith_pool_index);
    }
    int index_temp;
    for (index=0; index<len_pools; index++)
    {
        index_temp = index_list[index];
        ith_item.push_back(pools_temp[index][index_temp]);
    }
    return ith_item;
}

int Enumerator::findOccurenciesCount(const std::string& data, 
                                     const std::string& toSearch)
{
    // Get the first occurrence
    int count = 0;
    size_t pos = data.find(toSearch);

    // Repeat till end is reached
    while(pos != std::string::npos)
    {
        count++;
        // Get the next occurrence from the current position
        pos = data.find(toSearch, pos + toSearch.size());
    }
    return count;
}
