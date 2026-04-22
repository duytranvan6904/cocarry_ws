// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from human_hand_msgs:msg/HandState.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__TRAITS_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "human_hand_msgs/msg/detail/hand_state__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace human_hand_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const HandState & msg,
  std::ostream & out)
{
  out << "{";
  // member: header
  {
    out << "header: ";
    to_flow_style_yaml(msg.header, out);
    out << ", ";
  }

  // member: x
  {
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << ", ";
  }

  // member: y
  {
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << ", ";
  }

  // member: z
  {
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << ", ";
  }

  // member: tracking_id
  {
    out << "tracking_id: ";
    rosidl_generator_traits::value_to_yaml(msg.tracking_id, out);
    out << ", ";
  }

  // member: is_tracked
  {
    out << "is_tracked: ";
    rosidl_generator_traits::value_to_yaml(msg.is_tracked, out);
    out << ", ";
  }

  // member: confidence
  {
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << ", ";
  }

  // member: source
  {
    out << "source: ";
    rosidl_generator_traits::value_to_yaml(msg.source, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const HandState & msg,
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

  // member: x
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "x: ";
    rosidl_generator_traits::value_to_yaml(msg.x, out);
    out << "\n";
  }

  // member: y
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "y: ";
    rosidl_generator_traits::value_to_yaml(msg.y, out);
    out << "\n";
  }

  // member: z
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "z: ";
    rosidl_generator_traits::value_to_yaml(msg.z, out);
    out << "\n";
  }

  // member: tracking_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "tracking_id: ";
    rosidl_generator_traits::value_to_yaml(msg.tracking_id, out);
    out << "\n";
  }

  // member: is_tracked
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "is_tracked: ";
    rosidl_generator_traits::value_to_yaml(msg.is_tracked, out);
    out << "\n";
  }

  // member: confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.confidence, out);
    out << "\n";
  }

  // member: source
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "source: ";
    rosidl_generator_traits::value_to_yaml(msg.source, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const HandState & msg, bool use_flow_style = false)
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
  const human_hand_msgs::msg::HandState & msg,
  std::ostream & out, size_t indentation = 0)
{
  human_hand_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use human_hand_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const human_hand_msgs::msg::HandState & msg)
{
  return human_hand_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<human_hand_msgs::msg::HandState>()
{
  return "human_hand_msgs::msg::HandState";
}

template<>
inline const char * name<human_hand_msgs::msg::HandState>()
{
  return "human_hand_msgs/msg/HandState";
}

template<>
struct has_fixed_size<human_hand_msgs::msg::HandState>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<human_hand_msgs::msg::HandState>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<human_hand_msgs::msg::HandState>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__TRAITS_HPP_
