// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from motoros2_interfaces:msg/InitTrajEnum.idl
// generated code does not contain a copyright notice

#ifndef MOTOROS2_INTERFACES__MSG__DETAIL__INIT_TRAJ_ENUM__STRUCT_HPP_
#define MOTOROS2_INTERFACES__MSG__DETAIL__INIT_TRAJ_ENUM__STRUCT_HPP_

#include <algorithm>
#include <array>
#include <cstdint>
#include <memory>
#include <string>
#include <vector>

#include "rosidl_runtime_cpp/bounded_vector.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


#ifndef _WIN32
# define DEPRECATED__motoros2_interfaces__msg__InitTrajEnum __attribute__((deprecated))
#else
# define DEPRECATED__motoros2_interfaces__msg__InitTrajEnum __declspec(deprecated)
#endif

namespace motoros2_interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct InitTrajEnum_
{
  using Type = InitTrajEnum_<ContainerAllocator>;

  explicit InitTrajEnum_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = 0;
    }
  }

  explicit InitTrajEnum_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->value = 0;
    }
  }

  // field types and members
  using _value_type =
    uint16_t;
  _value_type value;

  // setters for named parameter idiom
  Type & set__value(
    const uint16_t & _arg)
  {
    this->value = _arg;
    return *this;
  }

  // constant declarations
  static constexpr uint16_t INIT_TRAJ_OK =
    0u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_OK_STR;
  static constexpr uint16_t INIT_TRAJ_UNSPECIFIED =
    200u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_UNSPECIFIED_STR;
  static constexpr uint16_t INIT_TRAJ_TOO_SMALL =
    201u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_TOO_SMALL_STR;
  static constexpr uint16_t INIT_TRAJ_TOO_BIG =
    202u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_TOO_BIG_STR;
  static constexpr uint16_t INIT_TRAJ_ALREADY_IN_MOTION =
    203u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_ALREADY_IN_MOTION_STR;
  static constexpr uint16_t INIT_TRAJ_INVALID_STARTING_POS =
    204u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_INVALID_STARTING_POS_STR;
  static constexpr uint16_t INIT_TRAJ_INVALID_VELOCITY =
    205u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_INVALID_VELOCITY_STR;
  static constexpr uint16_t INIT_TRAJ_INVALID_JOINTNAME =
    206u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_INVALID_JOINTNAME_STR;
  static constexpr uint16_t INIT_TRAJ_INCOMPLETE_JOINTLIST =
    207u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_INCOMPLETE_JOINTLIST_STR;
  static constexpr uint16_t INIT_TRAJ_INVALID_TIME =
    208u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_INVALID_TIME_STR;
  static constexpr uint16_t INIT_TRAJ_WRONG_MODE =
    209u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_WRONG_MODE_STR;
  static constexpr uint16_t INIT_TRAJ_BACKWARD_TIME =
    210u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_BACKWARD_TIME_STR;
  static constexpr uint16_t INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS =
    211u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR;
  static constexpr uint16_t INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES =
    212u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR;
  static constexpr uint16_t INIT_TRAJ_INVALID_ENDING_VELOCITY =
    213u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_INVALID_ENDING_VELOCITY_STR;
  static constexpr uint16_t INIT_TRAJ_INVALID_ENDING_ACCELERATION =
    214u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR;
  static constexpr uint16_t INIT_TRAJ_DUPLICATE_JOINT_NAME =
    215u;
  static const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>> INIT_TRAJ_DUPLICATE_JOINT_NAME_STR;

  // pointer types
  using RawPtr =
    motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator> *;
  using ConstRawPtr =
    const motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__motoros2_interfaces__msg__InitTrajEnum
    std::shared_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__motoros2_interfaces__msg__InitTrajEnum
    std::shared_ptr<motoros2_interfaces::msg::InitTrajEnum_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const InitTrajEnum_ & other) const
  {
    if (this->value != other.value) {
      return false;
    }
    return true;
  }
  bool operator!=(const InitTrajEnum_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct InitTrajEnum_

// alias to use template instance with default allocator
using InitTrajEnum =
  motoros2_interfaces::msg::InitTrajEnum_<std::allocator<void>>;

// constant definitions
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_OK;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_OK_STR = "OK";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_UNSPECIFIED;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_UNSPECIFIED_STR = "Unspecified failure";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_TOO_SMALL;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_TOO_SMALL_STR = "Trajectory must contain at least two points.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_TOO_BIG;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_TOO_BIG_STR = "Trajectory contains too many points (Not enough memory).";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_ALREADY_IN_MOTION;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_ALREADY_IN_MOTION_STR = "Already running a trajectory.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_STARTING_POS;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_STARTING_POS_STR = "The first point must match the robot's current position.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_VELOCITY;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_VELOCITY_STR = "The commanded velocity is too high.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_JOINTNAME;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_JOINTNAME_STR = "Invalid joint name specified. Check motoros2_config.yaml.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INCOMPLETE_JOINTLIST;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INCOMPLETE_JOINTLIST_STR = "Trajectory must contain data for all joints.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_TIME;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_TIME_STR = "Invalid time in trajectory.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_WRONG_MODE;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_WRONG_MODE_STR = "Must call start_traj_mode service";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_BACKWARD_TIME;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_BACKWARD_TIME_STR = "Trajectory message contains waypoints that are not strictly increasing in time.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR = "Trajectory did not contain position data for all axes.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR = "Trajectory did not contain velocity data for all axes.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_ENDING_VELOCITY;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_ENDING_VELOCITY_STR = "The final point in the trajectory must have zero velocity.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_ENDING_ACCELERATION;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR = "The final point in the trajectory must have zero acceleration.";
#if __cplusplus < 201703L
// static constexpr member variable definitions are only needed in C++14 and below, deprecated in C++17
template<typename ContainerAllocator>
constexpr uint16_t InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_DUPLICATE_JOINT_NAME;
#endif  // __cplusplus < 201703L
template<typename ContainerAllocator>
const std::basic_string<char, std::char_traits<char>, typename std::allocator_traits<ContainerAllocator>::template rebind_alloc<char>>
InitTrajEnum_<ContainerAllocator>::INIT_TRAJ_DUPLICATE_JOINT_NAME_STR = "The trajectory contains duplicate joint names.";

}  // namespace msg

}  // namespace motoros2_interfaces

#endif  // MOTOROS2_INTERFACES__MSG__DETAIL__INIT_TRAJ_ENUM__STRUCT_HPP_
