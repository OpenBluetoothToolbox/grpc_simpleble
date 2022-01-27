
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

set(INTERFACE_BUILD_DIR )
file(MAKE_DIRECTORY ${CMAKE_BINARY_DIR}/interface)
add_custom_target(
    interface
    COMMAND $<TARGET_FILE:protoc> -I proto --grpc_out ${CMAKE_BINARY_DIR}/interface --plugin=protoc-gen-grpc=$<TARGET_FILE:grpc_cpp_plugin> proto/simplegrpcble.proto
    COMMAND $<TARGET_FILE:protoc> -I proto --cpp_out ${CMAKE_BINARY_DIR}/interface proto/simplegrpcble.proto
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
)

add_executable(simplegrpcble server/main.cpp)
add_dependencies(simplegrpcble interface)

target_include_directories(simplegrpcble PRIVATE ${SIMPLEBLE_INCLUDES})
target_link_libraries(simplegrpcble PRIVATE simpleble-static libprotobuf grpc++_reflection grpc++)
