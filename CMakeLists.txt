cmake_minimum_required(VERSION 3.18)
project(node)
add_subdirectory(pybind11)
pybind11_add_module(node node.cpp)
