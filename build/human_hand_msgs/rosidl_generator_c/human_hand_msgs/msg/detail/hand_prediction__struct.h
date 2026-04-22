// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__STRUCT_H_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__STRUCT_H_

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
// Member 'model_name'
#include "rosidl_runtime_c/string.h"

/// Struct defined in msg/HandPrediction in the package human_hand_msgs.
/**
  * Predicted next hand position from ML model
 */
typedef struct human_hand_msgs__msg__HandPrediction
{
  std_msgs__msg__Header header;
  double x;
  double y;
  double z;
  double inference_time_ms;
  rosidl_runtime_c__String model_name;
  int32_t buffer_size;
  double prediction_confidence;
} human_hand_msgs__msg__HandPrediction;

// Struct for a sequence of human_hand_msgs__msg__HandPrediction.
typedef struct human_hand_msgs__msg__HandPrediction__Sequence
{
  human_hand_msgs__msg__HandPrediction * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} human_hand_msgs__msg__HandPrediction__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__STRUCT_H_
