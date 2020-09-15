# This is the setup script for cyGOURGS
# It runs some basic checks, then compiles the C++/Cython code
# Sohrab Towfighi 2020

set -e
# 1. Check python version
origversion=$(python -V 2>&1 | grep -Po '(?<=Python )(.+)')
version=$(echo "${origversion//./}")
version=${version:0:2}
if [[ $version -ne "38" ]] && [[ $version -ne "37" ]] && \
   [[ $version -ne "36" ]]; then
    echo "python version is invalid." 
    echo "Valid versions are 3.6.*, 3.7.*, 3.8.*" 
    echo "Version is: " $origversion
    echo "Going to try python3"
    origversion=$(python3 -V 2>&1 | grep -Po '(?<=Python )(.+)')
    version=$(echo "${origversion//./}")
    version=${version:0:2}
    if [[ $version -ne "38" ]] && [[ $version -ne "37" ]] && \
       [[ $version -ne "36" ]]; then
        exit 125
    fi
fi

# 2. Compile the main.exe, demonstrating that codes of core functionality compile
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    sudo apt-get install libboost-all-dev
    g++ -std=c++11 -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    . ./boost_path.py  # $path_to_boost variable is defined in ./boost_path.py
    g++ -std=c++11 -I $path_to_boost -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
fi

# 3. Compile the Cython code
python setup.py build_ext --inplace
echo "Completed installation without errors"