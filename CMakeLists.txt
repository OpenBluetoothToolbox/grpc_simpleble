
# Basic CMake configuration
cmake_minimum_required(VERSION 3.16.0)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(grpc_simpleble)

# Nice hack to automatically ignore the build directory
file(WRITE ${CMAKE_BINARY_DIR}/.gitignore "*")

# Include all necessary CMake modules
include(FetchContent)

set(SIMPLEBLE_GIT_REPOSITORY "https://github.com/OpenBluetoothToolbox/SimpleBLE.git")
set(SIMPLEBLE_GIT_TAG "v0.1.0")
set(GRPC_GIT_REPOSITORY "https://github.com/grpc/grpc.git")
set(GRPC_GIT_TAG "v1.43.2")

FetchContent_Declare(
    simpleble
    GIT_REPOSITORY ${SIMPLEBLE_GIT_REPOSITORY}
    GIT_TAG ${SIMPLEBLE_GIT_TAG}
)
FetchContent_MakeAvailable(simpleble)

FetchContent_Declare(
    grpc
    GIT_REPOSITORY ${GRPC_GIT_REPOSITORY}
    GIT_TAG ${GRPC_GIT_TAG}
)
FetchContent_MakeAvailable(grpc)

# Build all the necessary Protobuf and GRPC dependencies
set(INTERFACE_BUILD_DIR ${CMAKE_BINARY_DIR}/interface)
add_custom_target(
    interface
    COMMAND ${CMAKE_COMMAND} -E make_directory ${INTERFACE_BUILD_DIR}
    COMMAND $<TARGET_FILE:protoc> -I proto --grpc_out ${INTERFACE_BUILD_DIR} --plugin=protoc-gen-grpc=$<TARGET_FILE:grpc_cpp_plugin> proto/simplegrpcble.proto
    COMMAND $<TARGET_FILE:protoc> -I proto --cpp_out ${INTERFACE_BUILD_DIR} proto/simplegrpcble.proto
    BYPRODUCTS ${INTERFACE_BUILD_DIR}/simplegrpcble.pb.cc ${INTERFACE_BUILD_DIR}/simplegrpcble.pb.h ${INTERFACE_BUILD_DIR}/simplegrpcble.grpc.pb.cc ${INTERFACE_BUILD_DIR}/simplegrpcble.grpc.pb.h 
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
    DEPENDS protoc grpc_cpp_plugin
)

# Build the GRPC C++ server
add_executable(
    simplegrpcble_server
    server/main.cpp
    ${INTERFACE_BUILD_DIR}/simplegrpcble.pb.cc
    ${INTERFACE_BUILD_DIR}/simplegrpcble.grpc.pb.cc
)
add_dependencies(simplegrpcble_server interface)
target_include_directories(
    simplegrpcble_server PRIVATE
    ${SIMPLEBLE_INCLUDES}
    ${grpc_SOURCE_DIR}/include
    ${INTERFACE_BUILD_DIR}
)
target_link_libraries(simplegrpcble_server PRIVATE simpleble-static libprotobuf grpc++_reflection grpc++)

# Build the GRPC C++ client
