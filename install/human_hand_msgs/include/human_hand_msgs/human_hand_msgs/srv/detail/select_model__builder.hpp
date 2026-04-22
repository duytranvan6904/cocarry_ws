// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from human_hand_msgs:srv/SelectModel.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__BUILDER_HPP_
#define HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "human_hand_msgs/srv/detail/select_model__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace human_hand_msgs
{

namespace srv
{

namespace builder
{

class Init_SelectModel_Request_model_name
{
public:
  Init_SelectModel_Request_model_name()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::human_hand_msgs::srv::SelectModel_Request model_name(::human_hand_msgs::srv::SelectModel_Request::_model_name_type arg)
  {
    msg_.model_name = std::move(arg);
    return std::move(msg_);
  }

private:
  ::human_hand_msgs::srv::SelectModel_Request msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::human_hand_msgs::srv::SelectModel_Request>()
{
  return human_hand_msgs::srv::builder::Init_SelectModel_Request_model_name();
}

}  // namespace human_hand_msgs


namespace human_hand_msgs
{

namespace srv
{

namespace builder
{

class Init_SelectModel_Response_active_model
{
public:
  explicit Init_SelectModel_Response_active_model(::human_hand_msgs::srv::SelectModel_Response & msg)
  : msg_(msg)
  {}
  ::human_hand_msgs::srv::SelectModel_Response active_model(::human_hand_msgs::srv::SelectModel_Response::_active_model_type arg)
  {
    msg_.active_model = std::move(arg);
    return std::move(msg_);
  }

private:
  ::human_hand_msgs::srv::SelectModel_Response msg_;
};

class Init_SelectModel_Response_message
{
public:
  explicit Init_SelectModel_Response_message(::human_hand_msgs::srv::SelectModel_Response & msg)
  : msg_(msg)
  {}
  Init_SelectModel_Response_active_model message(::human_hand_msgs::srv::SelectModel_Response::_message_type arg)
  {
    msg_.message = std::move(arg);
    return Init_SelectModel_Response_active_model(msg_);
  }

private:
  ::human_hand_msgs::srv::SelectModel_Response msg_;
};

class Init_SelectModel_Response_success
{
public:
  Init_SelectModel_Response_success()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_SelectModel_Response_message success(::human_hand_msgs::srv::SelectModel_Response::_success_type arg)
  {
    msg_.success = std::move(arg);
    return Init_SelectModel_Response_message(msg_);
  }

private:
  ::human_hand_msgs::srv::SelectModel_Response msg_;
};

}  // namespace builder

}  // namespace srv

template<typename MessageType>
auto build();

template<>
inline
auto build<::human_hand_msgs::srv::SelectModel_Response>()
{
  return human_hand_msgs::srv::builder::Init_SelectModel_Response_success();
}

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__BUILDER_HPP_
