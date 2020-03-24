//#include <QCoreApplication>
#include <enumerator.h>
#include <primitiveset.h>
#include <string>

using namespace std;

int main(int argc, char *argv[])
{
    //QCoreApplication a(argc, argv);
    PrimitiveSet ps;
    ps.add_operator("ant.if_food_ahead", 2);
    ps.add_operator("prog2", 2);
    ps.add_operator("prog3", 3);
    ps.add_variable("ant.move_forward()");
    ps.add_variable("ant.turn_left()");
    ps.add_variable("ant.turn_right()");
    Enumerator en;
    en.init(ps);
    int iters = 10;
    vector<int long> seeds;
    for(int i=0; i< iters; i++)
    {
        seeds.push_back(i);
    }
    vector<string> soln = en.uniform_random_global_search(1000,iters, seeds);
    for( int i = 0; i < soln.size();i++ )
    {
        printf("\nSolution no: %d\n %s\n", i , soln[i].c_str());
    }
    return 0;
}
