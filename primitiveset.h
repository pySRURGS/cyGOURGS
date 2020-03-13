#ifndef PRIMITIVESET_H
#define PRIMITIVESET_H

#include <algorithm>
#include <iostream>
#include <string>
#include <vector>
#include <cmath>
#include <map>
#include <boost/random.hpp>
#include <boost/multiprecision/cpp_int.hpp>


class PrimitiveSet
{
public:
    PrimitiveSet();

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
    void add_operator(const std::string& funct_name, int arity, const std::string& datatype="default");

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
    void add_variable(const std::string& variable, const std::string datatype="default");

//    A method that adds a fitting parameter to the list of terminals
//    stored in self._fitting_parameters.

//    Parameters
//    ----------
//    param_name : string
//        The name of the fitting parameter which acts as a terminal

//    Returns
//    -------
//    None
    void add_fitting_parameter( const std::string& fitting_parameter);


//    A method that returns the fitting parameters and variables as one list.

//    Parameters
//    ----------
//    None

//    Returns
//    -------
//    terminals : list (vector)
    std::vector<std::string> get_terminals();

//    A method that returns the arities permissible in this search.

//    Parameters
//    ----------
//    None

//    Returns
//    -------
//    arities : a sorted list of integers
    std::vector<int> get_arities();

    std::vector<std::string> get_operators(int arity);

    boost::multiprecision::cpp_int mempower(boost::multiprecision::cpp_int a, int b);

private:

    std::vector<int> extract_keys(std::map<int, std::vector<std::string>> const& input_map);

private:
    std::vector<std::string> m_variables;
    std::vector<std::string> m_fitting_parameters;
    std::map<int, std::vector<std::string>> m_operators_map;
    std::vector<std::string> m_names;
};

#endif // PRIMITIVESET_H
