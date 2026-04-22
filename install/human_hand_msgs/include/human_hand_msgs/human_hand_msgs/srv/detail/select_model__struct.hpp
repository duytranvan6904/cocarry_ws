// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from human_hand_msgs:srv/SelectModel.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__STRUCT_HPP_
#define HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__human_hand_msgs__srv__SelectModel_Request __attribute__((deprecated))
#else
# define DEPRECATED__human_hand_msgs__srv__SelectModel_Request __declspec(deprecated)
#endif

namespace human_hand_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SelectModel_Request_
{
  using Type = SelectModel_Request_<ContainerAllocator>;

  explicit SelectModel_Request_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->model_name = "";
    }
  }

  explicit SelectModel_Request_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : model_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->model_name = "";
    }
  }

  // field types and members
  using _model_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _model_name_type model_name;

  // setters for named parameter idiom
  Type & set__model_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->model_name = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator> *;
  using ConstRawPtr =
    const human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__human_hand_msgs__srv__SelectModel_Request
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__human_hand_msgs__srv__SelectModel_Request
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Request_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SelectModel_Request_ & other) const
  {
    if (this->model_name != other.model_name) {
      return false;
    }
    return true;
  }
  bool operator!=(const SelectModel_Request_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SelectModel_Request_

// alias to use template instance with default allocator
using SelectModel_Request =
  human_hand_msgs::srv::SelectModel_Request_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace human_hand_msgs


#ifndef _WIN32
# define DEPRECATED__human_hand_msgs__srv__SelectModel_Response __attribute__((deprecated))
#else
# define DEPRECATED__human_hand_msgs__srv__SelectModel_Response __declspec(deprecated)
#endif

namespace human_hand_msgs
{

namespace srv
{

// message struct
template<class ContainerAllocator>
struct SelectModel_Response_
{
  using Type = SelectModel_Response_<ContainerAllocator>;

  explicit SelectModel_Response_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->active_model = "";
    }
  }

  explicit SelectModel_Response_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : message(_alloc),
    active_model(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->success = false;
      this->message = "";
      this->active_model = "";
    }
  }

  // field types and members
  using _success_type =
    bool;
  _success_type success;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;
  using _active_model_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _active_model_type active_model;

  // setters for named parameter idiom
  Type & set__success(
    const bool & _arg)
  {
    this->success = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }
  Type & set__active_model(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->active_model = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator> *;
  using ConstRawPtr =
    const human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__human_hand_msgs__srv__SelectModel_Response
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__human_hand_msgs__srv__SelectModel_Response
    std::shared_ptr<human_hand_msgs::srv::SelectModel_Response_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SelectModel_Response_ & other) const
  {
    if (this->success != other.success) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    if (this->active_model != other.active_model) {
      return false;
    }
    return true;
  }
  bool operator!=(const SelectModel_Response_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SelectModel_Response_

// alias to use template instance with default allocator
using SelectModel_Response =
  human_hand_msgs::srv::SelectModel_Response_<std::allocator<void>>;

// constant definitions

}  // namespace srv

}  // namespace human_hand_msgs

namespace human_hand_msgs
{

namespace srv
{

struct SelectModel
{
  using Request = human_hand_msgs::srv::SelectModel_Request;
  using Response = human_hand_msgs::srv::SelectModel_Response;
};

}  // namespace srv

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__SRV__DETAIL__SELECT_MODEL__STRUCT_HPP_
