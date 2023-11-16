# Note: CMake and this file are not neccessary to build and install Breathe.
# This exists to aid in development.

cmake_minimum_required(VERSION 3.26)
project(doxyparse LANGUAGES C)

find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module)
#find_package(Python3 REQUIRED COMPONENTS Interpreter Development.Module Development.SABIModule)
find_package(EXPAT)

set(module_name parser)

if (MSVC)
    add_compile_options(/W4)
else()
    add_compile_options(-Wall -Wextra -Werror=implicit-function-declaration)
endif()

add_custom_command(
    OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/${module_name}.c ${CMAKE_CURRENT_SOURCE_DIR}/stubs_template.pyi
    COMMAND Python3::Interpreter
        ${CMAKE_CURRENT_SOURCE_DIR}/make_parser.py
        ${CMAKE_CURRENT_SOURCE_DIR}/schema.json
        ${CMAKE_CURRENT_SOURCE_DIR}/module_template.c
        ${CMAKE_CURRENT_SOURCE_DIR}/stubs_template.pyi
        ${CMAKE_CURRENT_BINARY_DIR}/${module_name}.c
        ${CMAKE_CURRENT_BINARY_DIR}/${module_name}.pyi
    DEPENDS
        ${CMAKE_CURRENT_SOURCE_DIR}/make_parser.py
        ${CMAKE_CURRENT_SOURCE_DIR}/schema.json
        ${CMAKE_CURRENT_SOURCE_DIR}/module_template.c
        ${CMAKE_CURRENT_SOURCE_DIR}/stubs_template.pyi
    VERBATIM)

Python3_add_library(${module_name} MODULE WITH_SOABI ${CMAKE_CURRENT_BINARY_DIR}/${module_name}.c)
#Python3_add_library(${module_name} MODULE USE_SABI 3.7 WITH_SOABI ${CMAKE_CURRENT_BINARY_DIR}/${module_name}.c)
target_link_libraries(${module_name} PRIVATE EXPAT::EXPAT)
target_compile_definitions(${module_name} PRIVATE MODULE_NAME=${module_name})
