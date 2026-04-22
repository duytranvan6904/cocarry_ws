// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__BUILDER_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "human_hand_msgs/msg/detail/hand_prediction__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace human_hand_msgs
{

namespace msg
{

namespace builder
{

class Init_HandPrediction_prediction_confidence
{
public:
  explicit Init_HandPrediction_prediction_confidence(::human_hand_msgs::msg::HandPrediction & msg)
  : msg_(msg)
  {}
  ::human_hand_msgs::msg::HandPrediction prediction_confidence(::human_hand_msgs::msg::HandPrediction::_prediction_confidence_type arg)
  {
    msg_.prediction_confidence = std::move(arg);
    return std::move(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

class Init_HandPrediction_buffer_size
{
public:
  explicit Init_HandPrediction_buffer_size(::human_hand_msgs::msg::HandPrediction & msg)
  : msg_(msg)
  {}
  Init_HandPrediction_prediction_confidence buffer_size(::human_hand_msgs::msg::HandPrediction::_buffer_size_type arg)
  {
    msg_.buffer_size = std::move(arg);
    return Init_HandPrediction_prediction_confidence(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

class Init_HandPrediction_model_name
{
public:
  explicit Init_HandPrediction_model_name(::human_hand_msgs::msg::HandPrediction & msg)
  : msg_(msg)
  {}
  Init_HandPrediction_buffer_size model_name(::human_hand_msgs::msg::HandPrediction::_model_name_type arg)
  {
    msg_.model_name = std::move(arg);
    return Init_HandPrediction_buffer_size(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

class Init_HandPrediction_inference_time_ms
{
public:
  explicit Init_HandPrediction_inference_time_ms(::human_hand_msgs::msg::HandPrediction & msg)
  : msg_(msg)
  {}
  Init_HandPrediction_model_name inference_time_ms(::human_hand_msgs::msg::HandPrediction::_inference_time_ms_type arg)
  {
    msg_.inference_time_ms = std::move(arg);
    return Init_HandPrediction_model_name(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

class Init_HandPrediction_z
{
public:
  explicit Init_HandPrediction_z(::human_hand_msgs::msg::HandPrediction & msg)
  : msg_(msg)
  {}
  Init_HandPrediction_inference_time_ms z(::human_hand_msgs::msg::HandPrediction::_z_type arg)
  {
    msg_.z = std::move(arg);
    return Init_HandPrediction_inference_time_ms(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

class Init_HandPrediction_y
{
public:
  explicit Init_HandPrediction_y(::human_hand_msgs::msg::HandPrediction & msg)
  : msg_(msg)
  {}
  Init_HandPrediction_z y(::human_hand_msgs::msg::HandPrediction::_y_type arg)
  {
    msg_.y = std::move(arg);
    return Init_HandPrediction_z(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

class Init_HandPrediction_x
{
public:
  explicit Init_HandPrediction_x(::human_hand_msgs::msg::HandPrediction & msg)
  : msg_(msg)
  {}
  Init_HandPrediction_y x(::human_hand_msgs::msg::HandPrediction::_x_type arg)
  {
    msg_.x = std::move(arg);
    return Init_HandPrediction_y(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

class Init_HandPrediction_header
{
public:
  Init_HandPrediction_header()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_HandPrediction_x header(::human_hand_msgs::msg::HandPrediction::_header_type arg)
  {
    msg_.header = std::move(arg);
    return Init_HandPrediction_x(msg_);
  }

private:
  ::human_hand_msgs::msg::HandPrediction msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::human_hand_msgs::msg::HandPrediction>()
{
  return human_hand_msgs::msg::builder::Init_HandPrediction_header();
}

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__BUILDER_HPP_
