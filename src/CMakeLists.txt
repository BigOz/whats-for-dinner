cmake_minimum_required(VERSION 2.8)
project( BuildDatabase )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( BuildDatabase build_database.cpp )
target_link_libraries( BuildDatabase ${OpenCV_LIBS} )
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")
