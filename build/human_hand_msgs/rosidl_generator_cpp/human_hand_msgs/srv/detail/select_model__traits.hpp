// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from human_hand_msgs:srv/SelectModel.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__TRAITS_HPP_
#define HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "human_hand_msgs/srv/detail/select_model__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace human_hand_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const SelectModel_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: model_name
  {
    out << "model_name: ";
    rosidl_generator_traits::value_to_yaml(msg.model_name, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SelectModel_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: model_name
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "model_name: ";
    rosidl_generator_traits::value_to_yaml(msg.model_name, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SelectModel_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace human_hand_msgs

namespace rosidl_generator_traits
{

[[deprecated("use human_hand_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const human_hand_msgs::srv::SelectModel_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  human_hand_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use human_hand_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const human_hand_msgs::srv::SelectModel_Request & msg)
{
  return human_hand_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<human_hand_msgs::srv::SelectModel_Request>()
{
  return "human_hand_msgs::srv::SelectModel_Request";
}

template<>
inline const char * name<human_hand_msgs::srv::SelectModel_Request>()
{
  return "human_hand_msgs/srv/SelectModel_Request";
}

template<>
struct has_fixed_size<human_hand_msgs::srv::SelectModel_Request>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<human_hand_msgs::srv::SelectModel_Request>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<human_hand_msgs::srv::SelectModel_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace human_hand_msgs
{

namespace srv
{

inline void to_flow_style_yaml(
  const SelectModel_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: success
  {
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
    out << ", ";
  }

  // member: message
  {
    out << "message: ";
    rosidl_generator_traits::value_to_yaml(msg.message, out);
    out << ", ";
  }

  // member: active_model
  {
    out << "active_model: ";
    rosidl_generator_traits::value_to_yaml(msg.active_model, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const SelectModel_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: success
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "success: ";
    rosidl_generator_traits::value_to_yaml(msg.success, out);
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

  // member: active_model
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "active_model: ";
    rosidl_generator_traits::value_to_yaml(msg.active_model, out);
    out << "\n";
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const SelectModel_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace srv

}  // namespace human_hand_msgs

namespace rosidl_generator_traits
{

[[deprecated("use human_hand_msgs::srv::to_block_style_yaml() instead")]]
inline void to_yaml(
  const human_hand_msgs::srv::SelectModel_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  human_hand_msgs::srv::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use human_hand_msgs::srv::to_yaml() instead")]]
inline std::string to_yaml(const human_hand_msgs::srv::SelectModel_Response & msg)
{
  return human_hand_msgs::srv::to_yaml(msg);
}

template<>
inline const char * data_type<human_hand_msgs::srv::SelectModel_Response>()
{
  return "human_hand_msgs::srv::SelectModel_Response";
}

template<>
inline const char * name<human_hand_msgs::srv::SelectModel_Response>()
{
  return "human_hand_msgs/srv/SelectModel_Response";
}

template<>
struct has_fixed_size<human_hand_msgs::srv::SelectModel_Response>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<human_hand_msgs::srv::SelectModel_Response>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<human_hand_msgs::srv::SelectModel_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<human_hand_msgs::srv::SelectModel>()
{
  return "human_hand_msgs::srv::SelectModel";
}

template<>
inline const char * name<human_hand_msgs::srv::SelectModel>()
{
  return "human_hand_msgs/srv/SelectModel";
}

template<>
struct has_fixed_size<human_hand_msgs::srv::SelectModel>
  : std::integral_constant<
    bool,
    has_fixed_size<human_hand_msgs::srv::SelectModel_Request>::value &&
    has_fixed_size<human_hand_msgs::srv::SelectModel_Response>::value
  >
{
};

template<>
struct has_bounded_size<human_hand_msgs::srv::SelectModel>
  : std::integral_constant<
    bool,
    has_bounded_size<human_hand_msgs::srv::SelectModel_Request>::value &&
    has_bounded_size<human_hand_msgs::srv::SelectModel_Response>::value
  >
{
};

template<>
struct is_service<human_hand_msgs::srv::SelectModel>
  : std::true_type
{
};

template<>
struct is_service_request<human_hand_msgs::srv::SelectModel_Request>
  : std::true_type
{
};

template<>
struct is_service_response<human_hand_msgs::srv::SelectModel_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

#endif  // HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__TRAITS_HPP_
