#include "primitiveset.h"

using namespace std;
namespace mp = boost::multiprecision;

PrimitiveSet::PrimitiveSet()
{

}

void PrimitiveSet::add_operator(const std::string& funct_name, int arity, const std::string& datatype/*="default"*/)
{
    if (arity < 1)
    {
        std::cerr << "Invalid arity. Must be >= 1.";
        throw 3;
    }
    m_operators_map[arity].push_back(funct_name);
}
void PrimitiveSet::add_variable(const std::string& variable, const std::string datatype/*="default"*/)
{
    m_variables.push_back(variable);
}
void PrimitiveSet::add_fitting_parameter( const std::string& fitting_parameter)
{
    m_fitting_parameters.push_back(fitting_parameter);
}
std::vector<std::string> PrimitiveSet::get_terminals()
{
    vector<string> terminals;
    terminals.reserve(m_fitting_parameters.size() + m_variables.size());
    terminals.insert(terminals.end(), m_fitting_parameters.begin(),
                     m_fitting_parameters.end());
    terminals.insert(terminals.end(), m_variables.begin(),
                     m_variables.end());
    return terminals;
}

std::vector<int> PrimitiveSet::get_arities()
{
    /*
    A method that returns the arities permissible in this search.
    */
    vector<int> arities;
    arities = extract_keys(m_operators_map);
    return arities;
}

std::vector<std::string> PrimitiveSet::get_operators(int arity)
{
    return m_operators_map[arity];
}

vector<int> PrimitiveSet::extract_keys(map<int, vector<string>> const& input_map){
    /*
    Returns all the keys in a mapping of integers to vector<strings>
    */
    vector<int> retval;
    for (auto const& element : input_map){
        retval.push_back(element.first);
    }
    return retval;
}




