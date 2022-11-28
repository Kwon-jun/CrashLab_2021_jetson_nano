cmake_minimum_required(VERSION 3.0.2)
project(cam_sub)

## Compile as C++11, supported in ROS Kinetic and newer
# add_compile_options(-std=c++11)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  roscpp
  std_msgs
  darknet_ros_msgs
)

## System dependencies are found with CMake's conventions
# find_package(Boost REQUIRED COMPONENTS system)

include_directories(
# include
  ${catkin_INCLUDE_DIRS}
)

catkin_package(
	#INCLUDE_DIRS include
	#LIBRARIES cam_sub
	#CATKIN_DEPENDS roscpp std_msgs darknet_ros_msgs
	#DEPENDES system_lib 
)

add_executable(cam_sub_node src/cam_sub_node.cpp)

add_dependencies(cam_sub_node ${${PROJECT_NAME}_EXPORTED_TARGETS} ${catkin_EXPORTED_TARGETS})

target_link_libraries(cam_sub_node ${catkin_LIBRARIES})

