# compile the main.exe, demonstrating that codes of core functionality compile
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    : # do nothing
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW32_NT" ]; then
    path_to_boost=/c/boost/boost_1_72_0
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    path_to_boost=/c/boost/boost_1_72_0
fi

g++ -std=c++11 -I $path_to_boost -I . enumerator.cpp primitiveset.cpp main.cpp \
    -o main.exe
