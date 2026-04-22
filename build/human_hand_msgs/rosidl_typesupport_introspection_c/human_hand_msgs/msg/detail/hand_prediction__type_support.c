// generated from rosidl_typesupport_introspection_c/resource/idl__type_support.c.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice

#include <stddef.h>
#include "human_hand_msgs/msg/detail/hand_prediction__rosidl_typesupport_introspection_c.h"
#include "human_hand_msgs/msg/rosidl_typesupport_introspection_c__visibility_control.h"
#include "rosidl_typesupport_introspection_c/field_types.h"
#include "rosidl_typesupport_introspection_c/identifier.h"
#include "rosidl_typesupport_introspection_c/message_introspection.h"
#include "human_hand_msgs/msg/detail/hand_prediction__functions.h"
#include "human_hand_msgs/msg/detail/hand_prediction__struct.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/header.h"
// Member `header`
#include "std_msgs/msg/detail/header__rosidl_typesupport_introspection_c.h"
// Member `model_name`
#include "rosidl_runtime_c/string_functions.h"

#ifdef __cplusplus
extern "C"
{
#endif

void human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_init_function(
  void * message_memory, enum rosidl_runtime_c__message_initialization _init)
{
  // TODO(karsten1987): initializers are not yet implemented for typesupport c
  // see https://github.com/ros2/ros2/issues/397
  (void) _init;
  human_hand_msgs__msg__HandPrediction__init(message_memory);
}

void human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_fini_function(void * message_memory)
{
  human_hand_msgs__msg__HandPrediction__fini(message_memory);
}

static rosidl_typesupport_introspection_c__MessageMember human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_member_array[8] = {
  {
    "header",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_MESSAGE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message (initialized later)
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, header),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "x",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, x),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "y",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, y),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "z",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, z),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "inference_time_ms",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, inference_time_ms),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "model_name",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_STRING,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, model_name),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "buffer_size",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_INT32,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, buffer_size),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  },
  {
    "prediction_confidence",  // name
    rosidl_typesupport_introspection_c__ROS_TYPE_DOUBLE,  // type
    0,  // upper bound of string
    NULL,  // members of sub message
    false,  // is array
    0,  // array size
    false,  // is upper bound
    offsetof(human_hand_msgs__msg__HandPrediction, prediction_confidence),  // bytes offset in struct
    NULL,  // default value
    NULL,  // size() function pointer
    NULL,  // get_const(index) function pointer
    NULL,  // get(index) function pointer
    NULL,  // fetch(index, &value) function pointer
    NULL,  // assign(index, value) function pointer
    NULL  // resize(index) function pointer
  }
};

static const rosidl_typesupport_introspection_c__MessageMembers human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_members = {
  "human_hand_msgs__msg",  // message namespace
  "HandPrediction",  // message name
  8,  // number of fields
  sizeof(human_hand_msgs__msg__HandPrediction),
  human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_member_array,  // message members
  human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_init_function,  // function to initialize message memory (memory has to be allocated)
  human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_fini_function  // function to terminate message instance (will not free memory)
};

// this is not const since it must be initialized on first access
// since C does not allow non-integral compile-time constants
static rosidl_message_type_support_t human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_type_support_handle = {
  0,
  &human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_members,
  get_message_typesupport_handle_function,
};

ROSIDL_TYPESUPPORT_INTROSPECTION_C_EXPORT_human_hand_msgs
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, human_hand_msgs, msg, HandPrediction)() {
  human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_member_array[0].members_ =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, std_msgs, msg, Header)();
  if (!human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_type_support_handle.typesupport_identifier) {
    human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_type_support_handle.typesupport_identifier =
      rosidl_typesupport_introspection_c__identifier;
  }
  return &human_hand_msgs__msg__HandPrediction__rosidl_typesupport_introspection_c__HandPrediction_message_type_support_handle;
}
#ifdef __cplusplus
}
#endif
