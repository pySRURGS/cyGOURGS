# download the boost c++ package
current_dir=$pwd
wget -O ~/boost_1_72_0.tar.gz http://downloads.sourceforge.net/project/boost/boost/1.72.0/boost_1_72_0.tar.gz --no-check-certificate
tar  -C ~ -zxf ~/boost_1_72_0.tar.gz 
cd boost_1_72_0
./bootstrap.sh
./b2 install
cd $current_dir
# compile the main.exe, demonstrating that codes of core functionality compile
if [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then
    path_to_boost=~/boost_1_72_0
    g++ -std=c++11 -I $path_to_boost -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
elif [ "$(expr substr $(uname -s) 1 10)" == "MINGW64_NT" ]; then
    path_to_boost=~/boost_1_72_0
    g++ -std=c++11 -I $path_to_boost -I . enumerator.cpp primitiveset.cpp \
        main.cpp -o main.exe
fi
# Compile the Cython code
python setup.py build_ext --inplace

