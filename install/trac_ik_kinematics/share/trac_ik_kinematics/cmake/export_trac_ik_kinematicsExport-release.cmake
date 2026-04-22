#----------------------------------------------------------------
# Generated CMake target import file for configuration "Release".
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "trac_ik_kinematics::moveit_trac_ik_kinematics_plugin" for configuration "Release"
set_property(TARGET trac_ik_kinematics::moveit_trac_ik_kinematics_plugin APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
set_target_properties(trac_ik_kinematics::moveit_trac_ik_kinematics_plugin PROPERTIES
  IMPORTED_LOCATION_RELEASE "${_IMPORT_PREFIX}/lib/libmoveit_trac_ik_kinematics_plugin.so"
  IMPORTED_SONAME_RELEASE "libmoveit_trac_ik_kinematics_plugin.so"
  )

list(APPEND _IMPORT_CHECK_TARGETS trac_ik_kinematics::moveit_trac_ik_kinematics_plugin )
list(APPEND _IMPORT_CHECK_FILES_FOR_trac_ik_kinematics::moveit_trac_ik_kinematics_plugin "${_IMPORT_PREFIX}/lib/libmoveit_trac_ik_kinematics_plugin.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
