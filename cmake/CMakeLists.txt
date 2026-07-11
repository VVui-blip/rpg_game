cmake_minimum_required(VERSION 3.6)
project(main)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# File nay se duoc CI copy de vao app/jni/src/CMakeLists.txt cua khung SDL2 android-project.
# Khung do da co san add_subdirectory(SDL) o cap cha, nen chi can link "SDL2" la du.
add_library(main SHARED
    main.cpp
)

target_link_libraries(main SDL2)
