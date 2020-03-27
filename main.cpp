//#include <QCoreApplication>
#include <enumerator.h>
#include <primitiveset.h>
#include <string>

using namespace std;

int main(int argc, char *argv[])
{
    PrimitiveSet ps1;
    ps1.add_operator("ant.if_food_ahead", 2);
    ps1.add_operator("prog2", 2);
    ps1.add_operator("prog3", 3);
    ps1.add_variable("ant.move_forward()");
    ps1.add_variable("ant.turn_left()");
    ps1.add_variable("ant.turn_right()");
    Enumerator en1;
    en1.init(ps1);
    int iters = 10;
    vector<int long> seeds;
    for(int i=0; i< iters; i++)
    {
       seeds.push_back(i);
    }
    vector<string> soln1 = en1.uniform_random_global_search(1000, iters, seeds);
    for( int i = 0; i < soln1.size(); i++ )
    {
       printf("\nSolution no: %d\n %s\n", i , soln1[i].c_str());
    }
    PrimitiveSet ps;
    ps.add_operator("add", 2);
    ps.add_operator("sub", 1);
    ps.add_operator("truediv", 3);
    ps.add_operator("mul", 1);
    ps.add_variable("x");
    ps.add_variable("y");
    Enumerator en;
    en.init(ps);
    int i = 10000000;
    int n = i+1;
    int r_i = en.calculate_R_i(i);
    int s_i = en.calculate_S_i(i);
    int r = int(r_i/2);
    int s = int(s_i/2);
    string soln = en.generate_specified_solution(i,r,s,n);
    printf("\nSolution is: %s",soln.c_str());
    return 0;
}
