#include "enumerator.h"
#include "boost/algorithm/string/replace.hpp"
#include "time.h"

using namespace std;
namespace mp = boost::multiprecision;

Enumerator::Enumerator(PrimitiveSet& primitiveSet)
{
    m_primitiveSet = primitiveSet;
}

std::vector<std::string> Enumerator::uniform_random_global_search_once(int n, int num_iters)
{
    vector<string> soln;
    for(int i=0;i<num_iters;i++)
    {
        soln.push_back( uniform_random_global_search_once( n ) );
    }
    return soln;
}

string Enumerator::uniform_random_global_search_once(int n)
{
    //srand ( time(0) );
    int i = rand() % n;
    int r_i = calculate_R_i(i);
    int s_i = calculate_S_i(i);
    int r = rand() % r_i - 1;
    int s = rand() % s_i - 1;
    string candidate_solution = generate_specified_solution( i, r, s, n );
    return candidate_solution;
}

int Enumerator::calculate_R_i(int i)
{
    if ( i == 0 )
    {
        return 1;
    }
    int r_i = 1;
    vector<int> all_G_i_b = calculate_all_G_i_b(i);
    for(int ii = 0; ii < all_G_i_b.size(); ii++)
    {
        int g_i_b = all_G_i_b[ii];
        if( g_i_b != 0 )
        {
            r_i = r_i * g_i_b;
        }
    }
    return r_i;
}
int Enumerator::calculate_S_i(int i)
{
    int m = m_primitiveSet.get_terminals().size();
    int j_i = calculate_a_i(i);
    int S_i = (int)m_primitiveSet.mempower(m, j_i);
    return S_i;
}
vector<int> Enumerator::calculate_all_G_i_b(int i)
{
    vector<int> arities = m_primitiveSet.get_arities();
    int k = arities.size();
    vector<int> list_g_i_b;
    for(int b=0; b < k;b++)
    {
        list_g_i_b.push_back(calculate_G_i_b(i,b));
    }
    return list_g_i_b;
}

int Enumerator::calculate_G_i_b(int i, int b)
{
    vector<int> arities = m_primitiveSet.get_arities();
    int f_b = m_primitiveSet.get_operators(arities[b]).size();
    int l_i_b = calculate_l_i_b( i, b );
    mp::cpp_int G_i_b = m_primitiveSet.mempower(f_b, l_i_b );
    //:TODO: type conversion here
    return (int)G_i_b;
}

int Enumerator::calculate_l_i_b(int i, int b)
{
    vector<int> arities = m_primitiveSet.get_arities();
    int k = arities.size();
    int l_i_b;
    if( i == 0 )
    {
        l_i_b = 0;
    }
    else if ( 1 <= i && i <= k )
    {
        if( b == i - 1 )
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
        vector<int> e_base_arity = decimal_to_base_m(e,m);
        vector<vector<int>> list_bits = deinterleave(e_base_arity, m);
        vector<int> list_bits_deci;
        for(int u = 0; u < list_bits.size(); u++)
        {
            list_bits_deci.push_back(base_m_to_decimal(list_bits[u],m));
        }
        for(int ii = 0; ii < list_bits_deci.size(); ii++)
        {
            int i_deinterleave = list_bits_deci[ii];
            l_i_b += calculate_l_i_b(i_deinterleave, b );
        }
    }
    return l_i_b;
}

int Enumerator::calculate_a_i(int i)
{
    vector<int> arities;
    int k = arities.size();
    int a_i = 0;
    if( i == 0 )
    {
        a_i = 1;
    }
    else if ( 1 <= i && i <= k )
    {
        a_i = arities[i-1];
    }
    else
    {
        int e = (i - 1) / k;
        int j = (i - 1) % k;
        int m = arities[j];
        vector<int> e_base_arity = decimal_to_base_m(e,m);
        vector<vector<int>> list_bits = deinterleave(e_base_arity, m);
        vector<int> list_bits_deci;
        for(int u = 0; u < list_bits.size(); u++)
        {
            list_bits_deci.push_back(base_m_to_decimal(list_bits[u],m));
        }
        for(int ii = 0; ii < list_bits_deci.size(); ii++)
        {
            int i_deinterleave = list_bits_deci[ii];
            a_i += calculate_a_i(i_deinterleave);
        }
    }
}

string Enumerator::generate_specified_solution(int i, int r, int s, int n)
{
    int r_i = calculate_R_i(i);
    int s_i = calculate_S_i(i);
    if ( ( r >= r_i ) || (r < 0 ) )
    {
        cerr << "Enumerator::generate_specified_solution: invalid operator" << endl;
        return "";
    }
    if( ( s >= s_i )  || ( s < 0 ) )
    {
        cerr << "Enumerator::generate_specified_solution InvalidTreeIndex" << endl;
        return "";
    }
    if ( i > n )
    {
        cerr << "Enumerator::generate_specified_solution InvalidTreeIndex" << endl;
        return "";
    }
    string tree = ith_n_ary_tree(i);
    vector<int> g_i_b_values = calculate_all_G_i_b(i);
    vector<int> operator_config_indices; // todo unravel_index
    vector<vector<string>> operator_config;
    vector<int> arities = m_primitiveSet.get_arities();
    for(int b = 0; b < operator_config_indices.size(); b++ )
    {
        int z = operator_config_indices[b];
        int arity = arities[b];
        int l_i_b = calculate_l_i_b(i, b);
        vector<vector<string>> operators;
        operators.push_back( m_primitiveSet.get_operators( arity ) );
        vector<string> config = get_element_of_cartesian_product( operators, l_i_b, z );
        operator_config.push_back( config );
    }
    int a_i = calculate_a_i(i);
    vector<vector<string>> terminals;
    terminals.push_back( m_primitiveSet.get_terminals() );
    vector<string> terminal_config = get_element_of_cartesian_product( terminals, a_i, s );

    string workingTree = tree;
    string tempTree;
    int num_opers = std::count( tree.begin(), tree.end(), '[' );
    for( int ii = 0; ii < num_opers ; ii++ )
    {
        int start_index = workingTree.find_first_of('[');
        int arity = get_arity_of_term( start_index, workingTree );
        int index = -1;
        for( int jj = 0; jj < arities.size(); jj++ )
        {
            if( arities[jj] == arity )
            {
                index = jj;
                break;
            }
        }
        vector<string> operator_config_vector = operator_config[index];
        string my_operator = operator_config_vector[operator_config_vector.size()-1];
        tempTree = workingTree.substr(0, start_index );
        tempTree.append(my_operator); tempTree.append("("); tempTree.append(workingTree.substr(start_index+1,workingTree.length() - start_index - 1 ));
        workingTree = tempTree;
    }
    boost::replace_all( tempTree, "]", ")" );

    int num_terminals = std::count( workingTree.begin(), workingTree.end(), ".." );
    for( int ii = 0; ii < num_terminals; ii++)
    {
        string terminal = terminal_config[ii].substr(terminal_config[ii].size()-1,1);
        boost::replace_first( workingTree, "..", terminal );
    }
    tree = workingTree;
    return tree;

}



string Enumerator::ith_n_ary_tree(int i)
{
    vector<int> arities = m_primitiveSet.get_arities();
    string tree;
    int k = arities.size();
    if( i == 0 )
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
        string reverseTree = tree;
        std::reverse(reverseTree.begin(), reverseTree.end());
        tree = reverseTree + "]";
    }
    else
    {
        int e = (i - 1) / k;
        int j = (i - 1) % k;
        int m = arities[j];
        vector<int> e_base_arity = decimal_to_base_m(e,m);
        vector<vector<int>> list_bits = deinterleave(e_base_arity, m);
        vector<int> list_bits_deci;
        for(int u = 0; u < list_bits.size(); u++)
        {
            list_bits_deci.push_back(base_m_to_decimal(list_bits[u],m));
        }
        vector<string> subtrees;
        for(int x = 0; x < list_bits_deci.size(); x++)
        {
            subtrees.push_back(ith_n_ary_tree(list_bits_deci[x]));
        }
        tree = "[";
        tree.append(",");
        for(int j = 0; j < subtrees.size(); j++)
        {
            tree.append(subtrees[j]);
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
    if (tree.c_str()[start_index] == '[' )
    {
        cerr << "Start index must point to a square bracket";
        throw 2;
    }
    int len_solution = tree.length();
    for (int i=start_index; i<len_solution; i++)
    {
        if ( tree.c_str()[i] == '[' )
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

vector<int> Enumerator::decimal_to_base_m(int v, int m)
{
    vector<int> result;
    if( v < 0 )
    {
        cerr << "decimal_to_base_m: Do not supply negative values" << endl;
        return result;
    }
    if (v == 0)
    {
        result.push_back(0);
        return result;
    }
    if (m == 1)
    {
        for( int i = 0; i < v; i++ )
        {
            result.push_back(1);
        }
    }
    else if( m >= 2 )
    {
        result = numberToBase(v, m);
    }
    else
    {
        cerr << "Invalid m" << endl;
    }
    return result;

}
vector<int> Enumerator::numberToBase(int n, int b)
{
    vector<int> digits;
    if (n == 0)
    {
        digits.push_back(0);
        return digits;
    }
    while ( n != 0 )
    {
        digits.push_back(n % b);
        n /= b;
    }
     std::reverse(digits.begin(), digits.end());
     return digits;
}

int Enumerator::base_m_to_decimal(const std::vector<int>& v, int m)
{
   int result = 0;
   if (m == 1)
   {
       for(int i=0; i<v.size();i++)
       {
           result = result + v[i];
       }
   }
   else if (m>=2)
   {
       vector<int> reverse_number = v;
       std::reverse(reverse_number.begin(), reverse_number.end());
       for(int i = 0; i < reverse_number.size(); i++)
       {
            result += reverse_number[i] * pow(m,i);
       }
   }
   return result;
}

vector<vector<int>> Enumerator::deinterleave(vector<int> num, int m)
{
    vector<vector<int>> elements;
    for(int i = 0; i < m; i++ )
    {
        vector<int> empty;
        elements.push_back(empty);
    }
    while( ( num.size() % m ) != 0)
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
    return elements;
}


int Enumerator::countFreq(const string &pat, const string &txt){
    /*
        Given a input string and a substring.
        Find the frequency of occurrences of substring in given string.
    */
    int M = pat.length();
    int N = txt.length();
    int res = 0;
    /* A loop to slide pat[] one by one */
    for (int i = 0; i <= N - M; i++)
    {
        /* For current index i, check for
           pattern match */
        int j;
        for (j = 0; j < M; j++)
            if (txt[i+j] != pat[j])
                break;

        // if pat[0...M-1] = txt[i, i+1, ...i+M-1]
        if (j == M)
        {
           res++;
           j = 0;
        }
    }
    return res;
}


int Enumerator::count_nodes_in_tree(const string& tree){
    /*
        Given an n-ary tree in string format,
        counts the number of nodes in the tree
    */
    int n_terminals;
    int n_operators;
    int n_nodes;
    string operator_string = "[";
    string terminal_string = "..";
    n_operators = countFreq(operator_string, tree);
    n_terminals = countFreq(terminal_string, tree);
    n_nodes = n_terminals + n_operators;
    return n_nodes;
}

vector<string> Enumerator::get_element_of_cartesian_product(vector<vector<string>> pools,
                                                int repeat,
                                                int index){
    int len_product;
    int len_pools;
    int ith_pool_index = 0;
    int denominator = 1;
    int index_temp;
    int i;
    int k;
    int j;
    vector<vector<string>> pools_temp;
    vector<string> ith_item;
    vector<int> index_list;

    len_product = pools[0].size();
    len_pools = pools.size();
    for (j=1; j<len_pools; j++)
    {
        len_product = len_product * pools[j].size();
    }
    for (i=0; i<repeat; i++)
    {
        pools_temp[i].insert(pools_temp[i].end(),
                             pools[i].begin(),
                             pools[i].end());
    }
    pools = pools_temp;
    if (index >= len_product)
    {
        cerr << "index + 1 is bigger than the length of the product";
        throw 2;
    }
    for (j=0; j<len_pools; j++)
    {
        ith_pool_index = index;
        denominator = 1;
        for (k=j; k<len_pools; k++)
            {denominator = denominator * pools[k].size();}
        ith_pool_index = floor(ith_pool_index/denominator);
    }
    for (j=0; j<len_pools; j++)
    {
        for (k=j+1; k<len_pools; k++)
            {denominator = denominator * pools[k].size();}
        ith_pool_index = floor(ith_pool_index/denominator);
        if (j != 0)
            {ith_pool_index = ith_pool_index % pools[j].size();}
        index_list.push_back(ith_pool_index);
    }
    for (index=0; index<len_pools; index++)
    {
        index_temp = index_list[index];
        pools_temp[index] = pools[index];
        ith_item.push_back(pools_temp[index][index_temp]);
    }
    return ith_item;
}


