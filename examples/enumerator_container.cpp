#include "Enumerator.h"
#include "PrimitiveSet.h"

using namespace std;

static PrimitiveSet* s_primitiveSet = NULL;
static Enumerator* s_enumerator = NULL; 

void createEnumerator()
{
    if( !s_primitiveSet && !s_enumerator )
    {
        s_primitiveSet = new PrimitiveSet();
        s_enumerator = new Enumerator(s_primitiveSet);
    }
}

void add_operator( const string& a_operator, int arity )
{
    if( !s_primitiveSet || !s_enumerator )
    {
        cerr << "enumerator_container.cpp::add_operator: Enumerator not initialized" << endl;
        return;
    }
    s_primitiveSet->add_operator( a_operator, arity );
}

void add_variable( const string& a_variable )
{
    if( !s_primitiveSet || !s_enumerator )
    {
        cerr << "enumerator_container.cpp::add_variable: Enumerator not initialized" << endl;
        return;
    }
    s_primitiveSet->add_variable( a_variable );
}

string uniform_random_global_search_once(int n)
{
    return s_enumerator->uniform_random_global_search_once( n );
}
