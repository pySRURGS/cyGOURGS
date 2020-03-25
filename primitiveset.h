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

    const std::map<int, std::vector<std::string>>& get_operators_map();
    const std::vector<std::string>& get_variables();
    const std::vector<std::string>& get_fitting_parameters();
    const std::vector<std::string>& get_names();

    void set_operators_map(const std::map<int, std::vector<std::string>>& operators_map);
    void set_variables(const std::vector<std::string>& variables);
    void set_fitting_parameters(const std::vector<std::string>& fitting_parameters);
    void set_names(const std::vector<std::string>& names);
    
private:
    std::vector<int> extract_keys(std::map<int, std::vector<std::string> > const& input_map);

    // class attributes
    std::map<int, std::vector<std::string> > m_operators_map;
    std::vector<std::string> m_fitting_parameters;
    std::vector<std::string> m_variables;
    std::vector<std::string> m_names;


};

#endif // PRIMITIVESET_H
