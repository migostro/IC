cmake_minimum_required(VERSION 3.18)
project(nodes)
add_subdirectory(pybind11)
pybind11_add_module(nodes node.cpp)
