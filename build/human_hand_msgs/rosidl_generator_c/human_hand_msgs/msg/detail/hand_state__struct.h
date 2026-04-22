// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from human_hand_msgs:msg/HandState.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__STRUCT_H_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__STRUCT_H_

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
// Member 'source'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/HandState in the package human_hand_msgs.
/**
  * Measured hand position from camera (world frame, post-calibration)
 */
typedef struct human_hand_msgs__msg__HandState
{
  std_msgs__msg__Header header;
  double x;
  double y;
  double z;
  uint64_t tracking_id;
  bool is_tracked;
  double confidence;
  rosidl_runtime_c__String source;
} human_hand_msgs__msg__HandState;

// Struct for a sequence of human_hand_msgs__msg__HandState.
typedef struct human_hand_msgs__msg__HandState__Sequence
{
  human_hand_msgs__msg__HandState * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} human_hand_msgs__msg__HandState__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__STRUCT_H_
