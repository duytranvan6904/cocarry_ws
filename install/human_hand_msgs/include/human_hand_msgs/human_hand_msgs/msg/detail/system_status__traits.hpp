// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from human_hand_msgs:msg/SystemStatus.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__TRAITS_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "human_hand_msgs/msg/detail/system_status__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace human_hand_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const SystemStatus & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: node_name
  {
    out << "node_name: ";
    rosidl_generator_traits::value_to_yaml(msg.node_name, out);
    out << ", ";
  }

  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: fps
  {
    out << "fps: ";
    rosidl_generator_traits::value_to_yaml(msg.fps, out);
    out << ", ";
  }

  // member: latency_ms
  {
    out << "latency_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.latency_ms, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SystemStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: header
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "header:\n";
    to_block_style_yaml(msg.header, out, indentation + 2);
  }

  // member: node_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "node_name: ";
    rosidl_generator_traits::value_to_yaml(msg.node_name, out);
    out << "\n";
  }

  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: fps
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "fps: ";
    rosidl_generator_traits::value_to_yaml(msg.fps, out);
    out << "\n";
  }

  // member: latency_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "latency_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.latency_ms, out);
    out << "\n";
  }

  // member: message
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SystemStatus & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace msg

}  // namespace human_hand_msgs

namespace rosidl_generator_traits
{

[[deprecated("use human_hand_msgs::msg::to_block_style_yaml() instead")]]
inline void to_yaml(
  const human_hand_msgs::msg::SystemStatus & msg,
  std::ostream & out, size_t indentation = 0)
{
  human_hand_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use human_hand_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const human_hand_msgs::msg::SystemStatus & msg)
{
  return human_hand_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<human_hand_msgs::msg::SystemStatus>()
{
  return "human_hand_msgs::msg::SystemStatus";
}

template<>
inline const char * name<human_hand_msgs::msg::SystemStatus>()
{
  return "human_hand_msgs/msg/SystemStatus";
}

template<>
struct has_fixed_size<human_hand_msgs::msg::SystemStatus>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<human_hand_msgs::msg::SystemStatus>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<human_hand_msgs::msg::SystemStatus>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__TRAITS_HPP_
