cmake_minimum_required(VERSION 3.8)
project(hc10dtp_simulation)

find_package(ament_cmake REQUIRED)

# Install scripts
install(PROGRAMS
  scripts/motoros2_mock_node.py
  DESTINATION lib/${PROJECT_NAME}
)

# Install launch files
install(DIRECTORY launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
