# compile the main.exe, demonstrating that codes of core functionality compile
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    # assuming that user has already installed libboost-all-dev
    g++ -std=c++11 -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    path_to_boost=/c/boost/boost_1_72_0
    g++ -std=c++11 -I $path_to_boost -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
fi

# now compile the cython code
# Tested on Python 3.6
python setup.py build_ext --inplace

