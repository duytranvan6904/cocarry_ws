// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from human_hand_msgs:msg/SystemStatus.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__STRUCT_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


// Include directives for member types
// Member 'header'
#include "std_msgs/msg/detail/header__struct.hpp"

#ifndef _WIN32
# define DEPRECATED__human_hand_msgs__msg__SystemStatus __attribute__((deprecated))
#else
# define DEPRECATED__human_hand_msgs__msg__SystemStatus __declspec(deprecated)
#endif

namespace human_hand_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct SystemStatus_
{
  using Type = SystemStatus_<ContainerAllocator>;

  explicit SystemStatus_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->node_name = "";
      this->status = "";
      this->fps = 0.0;
      this->latency_ms = 0.0;
      this->message = "";
    }
  }

  explicit SystemStatus_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    node_name(_alloc),
    status(_alloc),
    message(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->node_name = "";
      this->status = "";
      this->fps = 0.0;
      this->latency_ms = 0.0;
      this->message = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _node_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _node_name_type node_name;
  using _status_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _status_type status;
  using _fps_type =
    double;
  _fps_type fps;
  using _latency_ms_type =
    double;
  _latency_ms_type latency_ms;
  using _message_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _message_type message;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__node_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->node_name = _arg;
    return *this;
  }
  Type & set__status(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->status = _arg;
    return *this;
  }
  Type & set__fps(
    const double & _arg)
  {
    this->fps = _arg;
    return *this;
  }
  Type & set__latency_ms(
    const double & _arg)
  {
    this->latency_ms = _arg;
    return *this;
  }
  Type & set__message(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->message = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    human_hand_msgs::msg::SystemStatus_<ContainerAllocator> *;
  using ConstRawPtr =
    const human_hand_msgs::msg::SystemStatus_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::msg::SystemStatus_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::msg::SystemStatus_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__human_hand_msgs__msg__SystemStatus
    std::shared_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__human_hand_msgs__msg__SystemStatus
    std::shared_ptr<human_hand_msgs::msg::SystemStatus_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const SystemStatus_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->node_name != other.node_name) {
      return false;
    }
    if (this->status != other.status) {
      return false;
    }
    if (this->fps != other.fps) {
      return false;
    }
    if (this->latency_ms != other.latency_ms) {
      return false;
    }
    if (this->message != other.message) {
      return false;
    }
    return true;
  }
  bool operator!=(const SystemStatus_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct SystemStatus_

// alias to use template instance with default allocator
using SystemStatus =
  human_hand_msgs::msg::SystemStatus_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__SYSTEM_STATUS__STRUCT_HPP_
