// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__STRUCT_HPP_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__STRUCT_HPP_

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
# define DEPRECATED__human_hand_msgs__msg__HandPrediction __attribute__((deprecated))
#else
# define DEPRECATED__human_hand_msgs__msg__HandPrediction __declspec(deprecated)
#endif

namespace human_hand_msgs
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct HandPrediction_
{
  using Type = HandPrediction_<ContainerAllocator>;

  explicit HandPrediction_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_init)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->inference_time_ms = 0.0;
      this->model_name = "";
      this->buffer_size = 0l;
      this->prediction_confidence = 0.0;
    }
  }

  explicit HandPrediction_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  : header(_alloc, _init),
    model_name(_alloc)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->x = 0.0;
      this->y = 0.0;
      this->z = 0.0;
      this->inference_time_ms = 0.0;
      this->model_name = "";
      this->buffer_size = 0l;
      this->prediction_confidence = 0.0;
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
  using _inference_time_ms_type =
    double;
  _inference_time_ms_type inference_time_ms;
  using _model_name_type =
    std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>;
  _model_name_type model_name;
  using _buffer_size_type =
    int32_t;
  _buffer_size_type buffer_size;
  using _prediction_confidence_type =
    double;
  _prediction_confidence_type prediction_confidence;

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
  Type & set__inference_time_ms(
    const double & _arg)
  {
    this->inference_time_ms = _arg;
    return *this;
  }
  Type & set__model_name(
    const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> & _arg)
  {
    this->model_name = _arg;
    return *this;
  }
  Type & set__buffer_size(
    const int32_t & _arg)
  {
    this->buffer_size = _arg;
    return *this;
  }
  Type & set__prediction_confidence(
    const double & _arg)
  {
    this->prediction_confidence = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    human_hand_msgs::msg::HandPrediction_<ContainerAllocator> *;
  using ConstRawPtr =
    const human_hand_msgs::msg::HandPrediction_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::msg::HandPrediction_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      human_hand_msgs::msg::HandPrediction_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__human_hand_msgs__msg__HandPrediction
    std::shared_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__human_hand_msgs__msg__HandPrediction
    std::shared_ptr<human_hand_msgs::msg::HandPrediction_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const HandPrediction_ & other) const
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
    if (this->inference_time_ms != other.inference_time_ms) {
      return false;
    }
    if (this->model_name != other.model_name) {
      return false;
    }
    if (this->buffer_size != other.buffer_size) {
      return false;
    }
    if (this->prediction_confidence != other.prediction_confidence) {
      return false;
    }
    return true;
  }
  bool operator!=(const HandPrediction_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct HandPrediction_

// alias to use template instance with default allocator
using HandPrediction =
  human_hand_msgs::msg::HandPrediction_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace human_hand_msgs

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__STRUCT_HPP_
