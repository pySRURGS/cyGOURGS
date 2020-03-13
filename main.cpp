#include <QCoreApplication>
#include <enumerator.h>
#include <primitiveset.h>
#include <string>

using namespace std;

int main(int argc, char *argv[])
{
    QCoreApplication a(argc, argv);
    PrimitiveSet ps;
    ps.add_operator("ant.if_food_ahead", 2);
    ps.add_operator("prog2", 2);
    ps.add_operator("prog3", 3);
    ps.add_variable("ant.move_forward()");
    ps.add_variable("ant.turn_left()");
    ps.add_variable("ant.turn_right()");
    Enumerator en(ps);
    vector<string> soln = en.uniform_random_global_search_once(1000,10);
    //printf("\nThe solution is\n, %s", soln.c_str());
    return a.exec();
}
