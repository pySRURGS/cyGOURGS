#include <string>

void createEnumerator();
void add_operator( const std::string& a_operator, int arity );
void add_variable( const std::string& a_variable );
std::string uniform_random_global_search_once(int n); 