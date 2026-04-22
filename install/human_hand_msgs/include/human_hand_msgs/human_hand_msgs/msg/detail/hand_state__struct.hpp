// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from human_hand_msgs:msg/HandState.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__STRUCT_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__STRUCT_HPP_

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
# define DEPRECATED__human_hand_msgs__msg__HandState __attribute__((deprecated))
#else
# define DEPRECATED__human_hand_msgs__msg__HandState __declspec(deprecated)
#endif

namespace human_hand_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct HandState_
{
  using Type = HandState_<ContainerAllocator>;

  explicit HandState_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->tracking_id = 0ull;
      this->is_tracked = false;
      this->confidence = 0.0;
      this->source = "";
    }
  }

  explicit HandState_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    source(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->tracking_id = 0ull;
      this->is_tracked = false;
      this->confidence = 0.0;
      this->source = "";
    }
  }

  // field types and members
  using _header_type =
    std_msgs::msg::Header_<ContainerAllocator>;
  _header_type header;
  using _x_type =
    double;
  _x_type x;
  using _y_type =
    double;
  _y_type y;
  using _z_type =
    double;
  _z_type z;
  using _tracking_id_type =
    uint64_t;
  _tracking_id_type tracking_id;
  using _is_tracked_type =
    bool;
  _is_tracked_type is_tracked;
  using _confidence_type =
    double;
  _confidence_type confidence;
  using _source_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _source_type source;

  // setters for named parameter idiom
  Type & set__header(
    const std_msgs::msg::Header_<ContainerAllocator> & _arg)
  {
    this->header = _arg;
    return *this;
  }
  Type & set__x(
    const double & _arg)
  {
    this->x = _arg;
    return *this;
  }
  Type & set__y(
    const double & _arg)
  {
    this->y = _arg;
    return *this;
  }
  Type & set__z(
    const double & _arg)
  {
    this->z = _arg;
    return *this;
  }
  Type & set__tracking_id(
    const uint64_t & _arg)
  {
    this->tracking_id = _arg;
    return *this;
  }
  Type & set__is_tracked(
    const bool & _arg)
  {
    this->is_tracked = _arg;
    return *this;
  }
  Type & set__confidence(
    const double & _arg)
  {
    this->confidence = _arg;
    return *this;
  }
  Type & set__source(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->source = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    human_hand_msgs::msg::HandState_<ContainerAllocator> *;
  using ConstRawPtr =
    const human_hand_msgs::msg::HandState_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::msg::HandState_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::msg::HandState_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__human_hand_msgs__msg__HandState
    std::shared_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__human_hand_msgs__msg__HandState
    std::shared_ptr<human_hand_msgs::msg::HandState_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const HandState_ & other) const
  {
    if (this->header != other.header) {
      return false;
    }
    if (this->x != other.x) {
      return false;
    }
    if (this->y != other.y) {
      return false;
    }
    if (this->z != other.z) {
      return false;
    }
    if (this->tracking_id != other.tracking_id) {
      return false;
    }
    if (this->is_tracked != other.is_tracked) {
      return false;
    }
    if (this->confidence != other.confidence) {
      return false;
    }
    if (this->source != other.source) {
      return false;
    }
    return true;
  }
  bool operator!=(const HandState_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct HandState_

// alias to use template instance with default allocator
using HandState =
  human_hand_msgs::msg::HandState_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_STATE__STRUCT_HPP_
