// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__TRAITS_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "human_hand_msgs/msg/detail/hand_prediction__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__traits.hpp"

namespace human_hand_msgs
{

namespace msg
{

inline void to_flow_style_yaml(
  const HandPrediction & msg,
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

  // member: inference_time_ms
  {
    out << "inference_time_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.inference_time_ms, out);
    out << ", ";
  }

  // member: model_name
  {
    out << "model_name: ";
    rosidl_generator_traits::value_to_yaml(msg.model_name, out);
    out << ", ";
  }

  // member: buffer_size
  {
    out << "buffer_size: ";
    rosidl_generator_traits::value_to_yaml(msg.buffer_size, out);
    out << ", ";
  }

  // member: prediction_confidence
  {
    out << "prediction_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.prediction_confidence, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const HandPrediction & msg,
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

  // member: inference_time_ms
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "inference_time_ms: ";
    rosidl_generator_traits::value_to_yaml(msg.inference_time_ms, out);
    out << "\n";
  }

  // member: model_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "model_name: ";
    rosidl_generator_traits::value_to_yaml(msg.model_name, out);
    out << "\n";
  }

  // member: buffer_size
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "buffer_size: ";
    rosidl_generator_traits::value_to_yaml(msg.buffer_size, out);
    out << "\n";
  }

  // member: prediction_confidence
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "prediction_confidence: ";
    rosidl_generator_traits::value_to_yaml(msg.prediction_confidence, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const HandPrediction & msg, bool use_flow_style = false)
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
  const human_hand_msgs::msg::HandPrediction & msg,
  std::ostream & out, size_t indentation = 0)
{
  human_hand_msgs::msg::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use human_hand_msgs::msg::to_yaml() instead")]]
inline std::string to_yaml(const human_hand_msgs::msg::HandPrediction & msg)
{
  return human_hand_msgs::msg::to_yaml(msg);
}

template<>
inline const char * data_type<human_hand_msgs::msg::HandPrediction>()
{
  return "human_hand_msgs::msg::HandPrediction";
}

template<>
inline const char * name<human_hand_msgs::msg::HandPrediction>()
{
  return "human_hand_msgs/msg/HandPrediction";
}

template<>
struct has_fixed_size<human_hand_msgs::msg::HandPrediction>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<human_hand_msgs::msg::HandPrediction>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<human_hand_msgs::msg::HandPrediction>
  : std::true_type {};

}  // namespace rosidl_generator_traits

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__TRAITS_HPP_
