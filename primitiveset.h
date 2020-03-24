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

    void add_operator(const std::string& funct_name, int arity);
    void add_variable(const std::string& variable);
    void add_fitting_parameter( const std::string& fitting_parameter );
    std::vector<std::string> get_terminals();
    std::vector<int> get_arities();
    std::vector<std::string> get_operators(int arity);
    std::vector<std::string> m_variables;
    std::vector<std::string> m_fitting_parameters;
    std::map<int, std::vector<std::string> > m_operators_map;
    
private:

    std::vector<int> extract_keys(
                     std::map<int, std::vector<std::string> > const& input_map);
    std::vector<std::string> m_names;
};

#endif // PRIMITIVESET_H
