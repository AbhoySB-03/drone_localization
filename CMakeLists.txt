cmake_minimum_required(VERSION 3.10.2 FATAL_ERROR)
project(radar_drone_simulation)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(ament_cmake REQUIRED)
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
# find_package(geometry_msgs REQUIRED)
# find_package(nlohmann_json REQUIRED)
# find_package(ignition-gazebo6 REQUIRED)
# find_package(ignition-plugin1 REQUIRED COMPONENTS register)
# find_package(ignition-msgs8 REQUIRED)
# find_package(ignition-transport11 REQUIRED)
# find_package(ignition-math6 REQUIRED)

# add_executable(waypoint_follower_node src/waypoint_follower_node.cpp)
# ament_target_dependencies(waypoint_follower_node rclcpp geometry_msgs nlohmann_json)

# install(TARGETS
#   waypoint_follower_node
#   DESTINATION lib/${PROJECT_NAME}
# )

# # Install sample waypoints.json if located in a config/ folder
# install(DIRECTORY 
#   config/
#   DESTINATION share/${PROJECT_NAME}/config
# )

# Candidate Gazebo releases, newest first:
#   sim package | plugin package | msgs package | transport package
# set(RADAR_FLAVORS
#   "gz-sim9|gz-plugin3|gz-msgs11|gz-transport14"   # Ionic
#   "gz-sim8|gz-plugin2|gz-msgs10|gz-transport13"   # Harmonic
#   "gz-sim7|gz-plugin2|gz-msgs9|gz-transport12"    # Garden
#   "ignition-gazebo6|ignition-plugin1|ignition-msgs8|ignition-transport11"  # Fortress
# )

# set(RADAR_FOUND FALSE)
# foreach(flavor ${RADAR_FLAVORS})
#   string(REPLACE "|" ";" parts "${flavor}")
#   list(GET parts 0 SIM)
#   list(GET parts 1 PLUG)
#   list(GET parts 2 MSGS)
#   list(GET parts 3 TRANS)
#   find_package(${SIM} QUIET)
#   if(${SIM}_FOUND)
#     find_package(${PLUG} REQUIRED COMPONENTS register)
#     find_package(${MSGS} REQUIRED)
#     find_package(${TRANS} REQUIRED)
#     set(RADAR_FOUND TRUE)
#     if(SIM MATCHES "^ignition")
#       set(RADAR_API_DEF RADAR_IGNITION_API)
#     else()
#       set(RADAR_API_DEF RADAR_GZ_API)
#     endif()
#     message(STATUS "radar_sim: building against ${SIM}")
#     break()
#   endif()
# endforeach()

# if(NOT RADAR_FOUND)
#   message(FATAL_ERROR "No supported Gazebo Sim installation found.")
# endif()

# add_library(RadarPlugin SHARED src/RadarPlugin.cc)
# target_compile_definitions(RadarPlugin PRIVATE ${RADAR_API_DEF})
# target_link_libraries(RadarPlugin PRIVATE
#   ${PLUG}::${PLUG}
#   ${SIM}::${SIM}
#   ${MSGS}::${MSGS}
#   ${TRANS}::${TRANS})



# add_library(NavSatNoisyPlugin SHARED src/NavSatNoisyPlugin.cc)
# target_link_libraries(NavSatNoisyPlugin
# ignition-gazebo6::ignition-gazebo6
# ignition-plugin1::ignition-plugin1
# ignition-msgs8::ignition-msgs8
# ignition-transport11::ignition-transport11
# ignition-math6::ignition-math6)

# install(TARGETS RadarPlugin
# LIBRARY DESTINATION lib/${PROJECT_NAME})

# install(TARGETS NavSatNoisyPlugin LIBRARY DESTINATION lib/${PROJECT_NAME})

# install(PROGRAMS
#   scripts/drone_ekf_node.py
#   scripts/odom_to_state_node.py
#   scripts/navsat_to_pos.py
#   DESTINATION lib/${PROJECT_NAME}
# )

install(DIRECTORY models worlds launch
  DESTINATION share/${PROJECT_NAME})

install(DIRECTORY lib/${PROJECT_NAME}

DESTINATION lib)


ament_package()