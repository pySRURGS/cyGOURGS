#include "primitiveset.h"

using namespace std;
namespace mp = boost::multiprecision;

PrimitiveSet::PrimitiveSet()
{

}

void PrimitiveSet::add_operator(const string& funct_name, int arity)
{
//    A method that adds a user-specified operator to the list of operators
//    stored in self._operators.

//    Parameters
//    ----------
//    func_name : string
//        The name of a function which will be used in the list of operators.

//    arity : integer
//        The number of inputs of the function `func_handle`

//    Returns
//    -------
//    None
    if (arity < 1)
    {
        std::cerr << "Invalid arity. Must be >= 1.";
        throw 3;
    }
    m_operators_map[arity].push_back(funct_name);
}

void PrimitiveSet::add_variable(const string& variable)
{
//    A method that adds a user-specified variable to the list of terminals
//    stored in self._variables.

//    Parameters
//    ----------
//    variable: str
//        The variable or value which will be used as a terminal. Its type
//        can be anything, but the operators will need to be able to take
//        `variable` as an input. Within pyGOURGS, it is treated as a string,
//        but will eventually be evaluated to whatever results from
//        `eval(variable)`.

//    Returns
//    -------
//    None
    m_variables.push_back(variable);
}

void PrimitiveSet::add_fitting_parameter(const std::string& fitting_parameter)
{    
//    A method that adds a fitting parameter to the list of terminals
//    stored in self._fitting_parameters.

//    Parameters
//    ----------
//    param_name : string
//        The name of the fitting parameter which acts as a terminal

//    Returns
//    -------
//    None
    m_fitting_parameters.push_back(fitting_parameter);
}

std::vector<std::string> PrimitiveSet::get_terminals()
{
//    A method that returns the fitting parameters and variables as one list.

//    Parameters
//    ----------
//    None

//    Returns
//    -------
//    terminals : list (vector)
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
//    A method that returns the arities permissible in this search.

//    Parameters
//    ----------
//    None

//    Returns
//    -------
//    arities : a sorted list of integers
    vector<int> arities;
    arities = extract_keys(m_operators_map);
    return arities;
}

std::vector<std::string> PrimitiveSet::get_operators(int arity)
{
    return m_operators_map[arity];
}

const std::map<int, std::vector<std::string>>& PrimitiveSet::get_operators_map()
{
    return m_operators_map;
}

const std::vector<std::string>&  PrimitiveSet::get_variables()
{
    return m_variables;
}

const std::vector<std::string>&  PrimitiveSet::get_fitting_parameters()
{
    return m_fitting_parameters;
}

const std::vector<std::string>&  PrimitiveSet::get_names()
{
    return m_variables;
}

void PrimitiveSet::set_operators_map(const std::map<int, std::vector<std::string>>& operators_map)
{
    m_operators_map = operators_map;
}
void PrimitiveSet::set_variables(const std::vector<std::string>& variables)
{
    m_variables = variables;
}
void PrimitiveSet::set_fitting_parameters(const std::vector<std::string>& fitting_parameters)
{
    m_fitting_parameters = fitting_parameters;
}
void PrimitiveSet::set_names(const std::vector<std::string>& names)
{
    m_names = names;
}

vector<int> PrimitiveSet::extract_keys(map<int, vector<string>> const& input_map)
{
    /*
    Returns all the keys in a mapping of integers to vector<strings>
    */
    vector<int> retval;
    for (auto const& element : input_map){
        retval.push_back(element.first);
    }
    return retval;
}




