// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from human_hand_msgs:srv/SelectModel.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__STRUCT_H_
#define HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'model_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SelectModel in the package human_hand_msgs.
typedef struct human_hand_msgs__srv__SelectModel_Request
{
  rosidl_runtime_c__String model_name;
} human_hand_msgs__srv__SelectModel_Request;

// Struct for a sequence of human_hand_msgs__srv__SelectModel_Request.
typedef struct human_hand_msgs__srv__SelectModel_Request__Sequence
{
  human_hand_msgs__srv__SelectModel_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} human_hand_msgs__srv__SelectModel_Request__Sequence;


// Constants defined in the message

// Include directives for member types
// Member 'message'
// Member 'active_model'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in srv/SelectModel in the package human_hand_msgs.
typedef struct human_hand_msgs__srv__SelectModel_Response
{
  bool success;
  rosidl_runtime_c__String message;
  rosidl_runtime_c__String active_model;
} human_hand_msgs__srv__SelectModel_Response;

// Struct for a sequence of human_hand_msgs__srv__SelectModel_Response.
typedef struct human_hand_msgs__srv__SelectModel_Response__Sequence
{
  human_hand_msgs__srv__SelectModel_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} human_hand_msgs__srv__SelectModel_Response__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__STRUCT_H_
