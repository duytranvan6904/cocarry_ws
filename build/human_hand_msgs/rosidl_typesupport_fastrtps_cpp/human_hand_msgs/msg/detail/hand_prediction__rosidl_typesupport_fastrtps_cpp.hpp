// generated from rosidl_typesupport_fastrtps_cpp/resource/idl__rosidl_typesupport_fastrtps_cpp.hpp.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_

#include "rosidl_runtime_c/message_type_support_struct.h"
#include "rosidl_typesupport_interface/macros.h"
#include "human_hand_msgs/msg/rosidl_typesupport_fastrtps_cpp__visibility_control.h"
#include "human_hand_msgs/msg/detail/hand_prediction__struct.hpp"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

#include "fastcdr/Cdr.h"

namespace human_hand_msgs
{

namespace msg
{

namespace typesupport_fastrtps_cpp
{

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_human_hand_msgs
cdr_serialize(
  const human_hand_msgs::msg::HandPrediction & ros_message,
  eprosima::fastcdr::Cdr & cdr);

bool
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_human_hand_msgs
cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  human_hand_msgs::msg::HandPrediction & ros_message);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_human_hand_msgs
get_serialized_size(
  const human_hand_msgs::msg::HandPrediction & ros_message,
  size_t current_alignment);

size_t
ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_human_hand_msgs
max_serialized_size_HandPrediction(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment);

}  // namespace typesupport_fastrtps_cpp

}  // namespace msg

}  // namespace human_hand_msgs

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_FASTRTPS_CPP_PUBLIC_human_hand_msgs
const rosidl_message_type_support_t *
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, human_hand_msgs, msg, HandPrediction)();

#ifdef __cplusplus
}
#endif

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__ROSIDL_TYPESUPPORT_FASTRTPS_CPP_HPP_
