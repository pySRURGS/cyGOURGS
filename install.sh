# compile the main.exe, demonstrating that codes of core functionality compile
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then    
    g++ -std=c++11 -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    path_to_boost=~/boost_1_72_0 #On Windows, users need to specify the path to boost
    g++ -std=c++11 -I $path_to_boost -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
fi
# Compile the Cython code
python setup.py build_ext --inplace

