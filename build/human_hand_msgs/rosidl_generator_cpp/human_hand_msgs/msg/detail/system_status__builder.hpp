// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from human_hand_msgs:msg/SystemStatus.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__BUILDER_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "human_hand_msgs/msg/detail/system_status__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace human_hand_msgs
{

namespace msg
{

namespace builder
{

class Init_SystemStatus_message
{
public:
  explicit Init_SystemStatus_message(::human_hand_msgs::msg::SystemStatus & msg)
  : msg_(msg)
  {}
  ::human_hand_msgs::msg::SystemStatus message(::human_hand_msgs::msg::SystemStatus::_message_type arg)
  {
    msg_.message = std::move(arg);
    return std::move(msg_);
  }

private:
  ::human_hand_msgs::msg::SystemStatus msg_;
};

class Init_SystemStatus_latency_ms
{
public:
  explicit Init_SystemStatus_latency_ms(::human_hand_msgs::msg::SystemStatus & msg)
  : msg_(msg)
  {}
  Init_SystemStatus_message latency_ms(::human_hand_msgs::msg::SystemStatus::_latency_ms_type arg)
  {
    msg_.latency_ms = std::move(arg);
    return Init_SystemStatus_message(msg_);
  }

private:
  ::human_hand_msgs::msg::SystemStatus msg_;
};

class Init_SystemStatus_fps
{
public:
  explicit Init_SystemStatus_fps(::human_hand_msgs::msg::SystemStatus & msg)
  : msg_(msg)
  {}
  Init_SystemStatus_latency_ms fps(::human_hand_msgs::msg::SystemStatus::_fps_type arg)
  {
    msg_.fps = std::move(arg);
    return Init_SystemStatus_latency_ms(msg_);
  }

private:
  ::human_hand_msgs::msg::SystemStatus msg_;
};

class Init_SystemStatus_status
{
public:
  explicit Init_SystemStatus_status(::human_hand_msgs::msg::SystemStatus & msg)
  : msg_(msg)
  {}
  Init_SystemStatus_fps status(::human_hand_msgs::msg::SystemStatus::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_SystemStatus_fps(msg_);
  }

private:
  ::human_hand_msgs::msg::SystemStatus msg_;
};

class Init_SystemStatus_node_name
{
public:
  explicit Init_SystemStatus_node_name(::human_hand_msgs::msg::SystemStatus & msg)
  : msg_(msg)
  {}
  Init_SystemStatus_status node_name(::human_hand_msgs::msg::SystemStatus::_node_name_type arg)
  {
    msg_.node_name = std::move(arg);
    return Init_SystemStatus_status(msg_);
  }

private:
  ::human_hand_msgs::msg::SystemStatus msg_;
};

class Init_SystemStatus_header
{
public:
  Init_SystemStatus_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SystemStatus_node_name header(::human_hand_msgs::msg::SystemStatus::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_SystemStatus_node_name(msg_);
  }

private:
  ::human_hand_msgs::msg::SystemStatus msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::human_hand_msgs::msg::SystemStatus>()
{
  return human_hand_msgs::msg::builder::Init_SystemStatus_header();
}

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__BUILDER_HPP_
