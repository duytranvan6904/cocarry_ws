// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from human_hand_msgs:msg/SystemStatus.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__STRUCT_H_
#define HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.h"
// Member 'node_name'
// Member 'status'
// Member 'message'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/SystemStatus in the package human_hand_msgs.
/**
  * System monitoring status
 */
typedef struct human_hand_msgs__msg__SystemStatus
{
  std_msgs__msg__Header header;
  rosidl_runtime_c__String node_name;
  rosidl_runtime_c__String status;
  double fps;
  double latency_ms;
  rosidl_runtime_c__String message;
} human_hand_msgs__msg__SystemStatus;

// Struct for a sequence of human_hand_msgs__msg__SystemStatus.
typedef struct human_hand_msgs__msg__SystemStatus__Sequence
{
  human_hand_msgs__msg__SystemStatus * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} human_hand_msgs__msg__SystemStatus__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__STRUCT_H_
