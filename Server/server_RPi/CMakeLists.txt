cmake_minimum_required (VERSION 2.8)
project(COA_PY_AutunomusCar)
set(CMAKE_MODULE_PATH "/usr/local/lib/cmake/${CMAKE_MODULE_PATH}")
include_directories(${PROJECT_SOURCE_DIR})
find_library(wiringPi_LIB wiringPi)
set(SOURCES Arduino.h SRasPi.h main.cpp )
set(THREADS_PREFER_PTHREAD_FLAG ON)
find_package(Threads REQUIRED)

add_executable (main ${SOURCES})

if(THREADS_HAVE_PTHREAD_ARG)
	target_compile_options(main PUBLIC "-pthread")
endif()
if(CMAKE_THREAD_LIBS_INIT)
	target_link_libraries (main "${CMAKE_THREAD_LIBS_INIT}")
endif()

target_link_libraries(main ${wiringPi_LIB})

