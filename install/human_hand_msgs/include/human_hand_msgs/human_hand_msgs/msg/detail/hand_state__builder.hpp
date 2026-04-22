// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from human_hand_msgs:msg/HandState.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__BUILDER_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "human_hand_msgs/msg/detail/hand_state__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace human_hand_msgs
{

namespace msg
{

namespace builder
{

class Init_HandState_source
{
public:
  explicit Init_HandState_source(::human_hand_msgs::msg::HandState & msg)
  : msg_(msg)
  {}
  ::human_hand_msgs::msg::HandState source(::human_hand_msgs::msg::HandState::_source_type arg)
  {
    msg_.source = std::move(arg);
    return std::move(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

class Init_HandState_confidence
{
public:
  explicit Init_HandState_confidence(::human_hand_msgs::msg::HandState & msg)
  : msg_(msg)
  {}
  Init_HandState_source confidence(::human_hand_msgs::msg::HandState::_confidence_type arg)
  {
    msg_.confidence = std::move(arg);
    return Init_HandState_source(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

class Init_HandState_is_tracked
{
public:
  explicit Init_HandState_is_tracked(::human_hand_msgs::msg::HandState & msg)
  : msg_(msg)
  {}
  Init_HandState_confidence is_tracked(::human_hand_msgs::msg::HandState::_is_tracked_type arg)
  {
    msg_.is_tracked = std::move(arg);
    return Init_HandState_confidence(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

class Init_HandState_tracking_id
{
public:
  explicit Init_HandState_tracking_id(::human_hand_msgs::msg::HandState & msg)
  : msg_(msg)
  {}
  Init_HandState_is_tracked tracking_id(::human_hand_msgs::msg::HandState::_tracking_id_type arg)
  {
    msg_.tracking_id = std::move(arg);
    return Init_HandState_is_tracked(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

class Init_HandState_z
{
public:
  explicit Init_HandState_z(::human_hand_msgs::msg::HandState & msg)
  : msg_(msg)
  {}
  Init_HandState_tracking_id z(::human_hand_msgs::msg::HandState::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_HandState_tracking_id(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

class Init_HandState_y
{
public:
  explicit Init_HandState_y(::human_hand_msgs::msg::HandState & msg)
  : msg_(msg)
  {}
  Init_HandState_z y(::human_hand_msgs::msg::HandState::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_HandState_z(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

class Init_HandState_x
{
public:
  explicit Init_HandState_x(::human_hand_msgs::msg::HandState & msg)
  : msg_(msg)
  {}
  Init_HandState_y x(::human_hand_msgs::msg::HandState::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_HandState_y(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

class Init_HandState_header
{
public:
  Init_HandState_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_HandState_x header(::human_hand_msgs::msg::HandState::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_HandState_x(msg_);
  }

private:
  ::human_hand_msgs::msg::HandState msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::human_hand_msgs::msg::HandState>()
{
  return human_hand_msgs::msg::builder::Init_HandState_header();
}

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__BUILDER_HPP_
