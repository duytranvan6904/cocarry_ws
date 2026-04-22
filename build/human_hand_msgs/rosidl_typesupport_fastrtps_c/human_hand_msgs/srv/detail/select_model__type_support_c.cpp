// generated from rosidl_typesupport_fastrtps_c/resource/idl__type_support_c.cpp.em
// with input from human_hand_msgs:srv/SelectModel.idl
// generated code does not contain a copyright notice
#include "human_hand_msgs/srv/detail/select_model__rosidl_typesupport_fastrtps_c.h"


#include <cassert>
#include <limits>
#include <string>
#include "rosidl_typesupport_fastrtps_c/identifier.h"
#include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
#include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
#include "human_hand_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "human_hand_msgs/srv/detail/select_model__struct.h"
#include "human_hand_msgs/srv/detail/select_model__functions.h"
#include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

#include "rosidl_runtime_c/string.h"  // model_name
#include "rosidl_runtime_c/string_functions.h"  // model_name

// forward declare type support functions


using _SelectModel_Request__ros_msg_type = human_hand_msgs__srv__SelectModel_Request;

static bool _SelectModel_Request__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _SelectModel_Request__ros_msg_type * ros_message = static_cast<const _SelectModel_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: model_name
  {
    const rosidl_runtime_c__String * str = &ros_message->model_name;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _SelectModel_Request__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _SelectModel_Request__ros_msg_type * ros_message = static_cast<_SelectModel_Request__ros_msg_type *>(untyped_ros_message);
  // Field name: model_name
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->model_name.data) {
      rosidl_runtime_c__String__init(&ros_message->model_name);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->model_name,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'model_name'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_human_hand_msgs
size_t get_serialized_size_human_hand_msgs__srv__SelectModel_Request(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SelectModel_Request__ros_msg_type * ros_message = static_cast<const _SelectModel_Request__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name model_name
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->model_name.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _SelectModel_Request__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_human_hand_msgs__srv__SelectModel_Request(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_human_hand_msgs
size_t max_serialized_size_human_hand_msgs__srv__SelectModel_Request(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: model_name
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = human_hand_msgs__srv__SelectModel_Request;
    is_plain =
      (
      offsetof(DataType, model_name) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _SelectModel_Request__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_human_hand_msgs__srv__SelectModel_Request(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SelectModel_Request = {
  "human_hand_msgs::srv",
  "SelectModel_Request",
  _SelectModel_Request__cdr_serialize,
  _SelectModel_Request__cdr_deserialize,
  _SelectModel_Request__get_serialized_size,
  _SelectModel_Request__max_serialized_size
};

static rosidl_message_type_support_t _SelectModel_Request__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SelectModel_Request,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, human_hand_msgs, srv, SelectModel_Request)() {
  return &_SelectModel_Request__type_support;
}

#if defined(__cplusplus)
}
#endif

// already included above
// #include <cassert>
// already included above
// #include <limits>
// already included above
// #include <string>
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "rosidl_typesupport_fastrtps_c/wstring_conversion.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_cpp/message_type_support.h"
// already included above
// #include "human_hand_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
// already included above
// #include "human_hand_msgs/srv/detail/select_model__struct.h"
// already included above
// #include "human_hand_msgs/srv/detail/select_model__functions.h"
// already included above
// #include "fastcdr/Cdr.h"

#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-parameter"
# ifdef __clang__
#  pragma clang diagnostic ignored "-Wdeprecated-register"
#  pragma clang diagnostic ignored "-Wreturn-type-c-linkage"
# endif
#endif
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif

// includes and forward declarations of message dependencies and their conversion functions

#if defined(__cplusplus)
extern "C"
{
#endif

// already included above
// #include "rosidl_runtime_c/string.h"  // active_model, message
// already included above
// #include "rosidl_runtime_c/string_functions.h"  // active_model, message

// forward declare type support functions


using _SelectModel_Response__ros_msg_type = human_hand_msgs__srv__SelectModel_Response;

static bool _SelectModel_Response__cdr_serialize(
  const void * untyped_ros_message,
  eprosima::fastcdr::Cdr & cdr)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  const _SelectModel_Response__ros_msg_type * ros_message = static_cast<const _SelectModel_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    cdr << (ros_message->success ? true : false);
  }

  // Field name: message
  {
    const rosidl_runtime_c__String * str = &ros_message->message;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  // Field name: active_model
  {
    const rosidl_runtime_c__String * str = &ros_message->active_model;
    if (str->capacity == 0 || str->capacity <= str->size) {
      fprintf(stderr, "string capacity not greater than size\n");
      return false;
    }
    if (str->data[str->size] != '\0') {
      fprintf(stderr, "string not null-terminated\n");
      return false;
    }
    cdr << str->data;
  }

  return true;
}

static bool _SelectModel_Response__cdr_deserialize(
  eprosima::fastcdr::Cdr & cdr,
  void * untyped_ros_message)
{
  if (!untyped_ros_message) {
    fprintf(stderr, "ros message handle is null\n");
    return false;
  }
  _SelectModel_Response__ros_msg_type * ros_message = static_cast<_SelectModel_Response__ros_msg_type *>(untyped_ros_message);
  // Field name: success
  {
    uint8_t tmp;
    cdr >> tmp;
    ros_message->success = tmp ? true : false;
  }

  // Field name: message
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->message.data) {
      rosidl_runtime_c__String__init(&ros_message->message);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->message,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'message'\n");
      return false;
    }
  }

  // Field name: active_model
  {
    std::string tmp;
    cdr >> tmp;
    if (!ros_message->active_model.data) {
      rosidl_runtime_c__String__init(&ros_message->active_model);
    }
    bool succeeded = rosidl_runtime_c__String__assign(
      &ros_message->active_model,
      tmp.c_str());
    if (!succeeded) {
      fprintf(stderr, "failed to assign string into field 'active_model'\n");
      return false;
    }
  }

  return true;
}  // NOLINT(readability/fn_size)

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_human_hand_msgs
size_t get_serialized_size_human_hand_msgs__srv__SelectModel_Response(
  const void * untyped_ros_message,
  size_t current_alignment)
{
  const _SelectModel_Response__ros_msg_type * ros_message = static_cast<const _SelectModel_Response__ros_msg_type *>(untyped_ros_message);
  (void)ros_message;
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  (void)padding;
  (void)wchar_size;

  // field.name success
  {
    size_t item_size = sizeof(ros_message->success);
    current_alignment += item_size +
      eprosima::fastcdr::Cdr::alignment(current_alignment, item_size);
  }
  // field.name message
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->message.size + 1);
  // field.name active_model
  current_alignment += padding +
    eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
    (ros_message->active_model.size + 1);

  return current_alignment - initial_alignment;
}

static uint32_t _SelectModel_Response__get_serialized_size(const void * untyped_ros_message)
{
  return static_cast<uint32_t>(
    get_serialized_size_human_hand_msgs__srv__SelectModel_Response(
      untyped_ros_message, 0));
}

ROSIDL_TYPESUPPORT_FASTRTPS_C_PUBLIC_human_hand_msgs
size_t max_serialized_size_human_hand_msgs__srv__SelectModel_Response(
  bool & full_bounded,
  bool & is_plain,
  size_t current_alignment)
{
  size_t initial_alignment = current_alignment;

  const size_t padding = 4;
  const size_t wchar_size = 4;
  size_t last_member_size = 0;
  (void)last_member_size;
  (void)padding;
  (void)wchar_size;

  full_bounded = true;
  is_plain = true;

  // member: success
  {
    size_t array_size = 1;

    last_member_size = array_size * sizeof(uint8_t);
    current_alignment += array_size * sizeof(uint8_t);
  }
  // member: message
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }
  // member: active_model
  {
    size_t array_size = 1;

    full_bounded = false;
    is_plain = false;
    for (size_t index = 0; index < array_size; ++index) {
      current_alignment += padding +
        eprosima::fastcdr::Cdr::alignment(current_alignment, padding) +
        1;
    }
  }

  size_t ret_val = current_alignment - initial_alignment;
  if (is_plain) {
    // All members are plain, and type is not empty.
    // We still need to check that the in-memory alignment
    // is the same as the CDR mandated alignment.
    using DataType = human_hand_msgs__srv__SelectModel_Response;
    is_plain =
      (
      offsetof(DataType, active_model) +
      last_member_size
      ) == ret_val;
  }

  return ret_val;
}

static size_t _SelectModel_Response__max_serialized_size(char & bounds_info)
{
  bool full_bounded;
  bool is_plain;
  size_t ret_val;

  ret_val = max_serialized_size_human_hand_msgs__srv__SelectModel_Response(
    full_bounded, is_plain, 0);

  bounds_info =
    is_plain ? ROSIDL_TYPESUPPORT_FASTRTPS_PLAIN_TYPE :
    full_bounded ? ROSIDL_TYPESUPPORT_FASTRTPS_BOUNDED_TYPE : ROSIDL_TYPESUPPORT_FASTRTPS_UNBOUNDED_TYPE;
  return ret_val;
}


static message_type_support_callbacks_t __callbacks_SelectModel_Response = {
  "human_hand_msgs::srv",
  "SelectModel_Response",
  _SelectModel_Response__cdr_serialize,
  _SelectModel_Response__cdr_deserialize,
  _SelectModel_Response__get_serialized_size,
  _SelectModel_Response__max_serialized_size
};

static rosidl_message_type_support_t _SelectModel_Response__type_support = {
  rosidl_typesupport_fastrtps_c__identifier,
  &__callbacks_SelectModel_Response,
  get_message_typesupport_handle_function,
};

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, human_hand_msgs, srv, SelectModel_Response)() {
  return &_SelectModel_Response__type_support;
}

#if defined(__cplusplus)
}
#endif

#include "rosidl_typesupport_fastrtps_cpp/service_type_support.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "rosidl_typesupport_fastrtps_c/identifier.h"
// already included above
// #include "human_hand_msgs/msg/rosidl_typesupport_fastrtps_c__visibility_control.h"
#include "human_hand_msgs/srv/select_model.h"

#if defined(__cplusplus)
extern "C"
{
#endif

static service_type_support_callbacks_t SelectModel__callbacks = {
  "human_hand_msgs::srv",
  "SelectModel",
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, human_hand_msgs, srv, SelectModel_Request)(),
  ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, human_hand_msgs, srv, SelectModel_Response)(),
};

static rosidl_service_type_support_t SelectModel__handle = {
  rosidl_typesupport_fastrtps_c__identifier,
  &SelectModel__callbacks,
  get_service_typesupport_handle_function,
};

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, human_hand_msgs, srv, SelectModel)() {
  return &SelectModel__handle;
}

#if defined(__cplusplus)
}
#endif
