// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from human_hand_msgs:msg/SystemStatus.idl
// generated code does not contain a copyright notice
#include "human_hand_msgs/msg/detail/system_status__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `node_name`
// Member `status`
// Member `message`
#include "rosidl_runtime_c/string_functions.h"

bool
human_hand_msgs__msg__SystemStatus__init(human_hand_msgs__msg__SystemStatus * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    human_hand_msgs__msg__SystemStatus__fini(msg);
    return false;
  }
  // node_name
  if (!rosidl_runtime_c__String__init(&msg->node_name)) {
    human_hand_msgs__msg__SystemStatus__fini(msg);
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__init(&msg->status)) {
    human_hand_msgs__msg__SystemStatus__fini(msg);
    return false;
  }
  // fps
  // latency_ms
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    human_hand_msgs__msg__SystemStatus__fini(msg);
    return false;
  }
  return true;
}

void
human_hand_msgs__msg__SystemStatus__fini(human_hand_msgs__msg__SystemStatus * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // node_name
  rosidl_runtime_c__String__fini(&msg->node_name);
  // status
  rosidl_runtime_c__String__fini(&msg->status);
  // fps
  // latency_ms
  // message
  rosidl_runtime_c__String__fini(&msg->message);
}

bool
human_hand_msgs__msg__SystemStatus__are_equal(const human_hand_msgs__msg__SystemStatus * lhs, const human_hand_msgs__msg__SystemStatus * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__are_equal(
      &(lhs->header), &(rhs->header)))
  {
    return false;
  }
  // node_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->node_name), &(rhs->node_name)))
  {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->status), &(rhs->status)))
  {
    return false;
  }
  // fps
  if (lhs->fps != rhs->fps) {
    return false;
  }
  // latency_ms
  if (lhs->latency_ms != rhs->latency_ms) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  return true;
}

bool
human_hand_msgs__msg__SystemStatus__copy(
  const human_hand_msgs__msg__SystemStatus * input,
  human_hand_msgs__msg__SystemStatus * output)
{
  if (!input || !output) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__copy(
      &(input->header), &(output->header)))
  {
    return false;
  }
  // node_name
  if (!rosidl_runtime_c__String__copy(
      &(input->node_name), &(output->node_name)))
  {
    return false;
  }
  // status
  if (!rosidl_runtime_c__String__copy(
      &(input->status), &(output->status)))
  {
    return false;
  }
  // fps
  output->fps = input->fps;
  // latency_ms
  output->latency_ms = input->latency_ms;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  return true;
}

human_hand_msgs__msg__SystemStatus *
human_hand_msgs__msg__SystemStatus__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__msg__SystemStatus * msg = (human_hand_msgs__msg__SystemStatus *)allocator.allocate(sizeof(human_hand_msgs__msg__SystemStatus), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(human_hand_msgs__msg__SystemStatus));
  bool success = human_hand_msgs__msg__SystemStatus__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
human_hand_msgs__msg__SystemStatus__destroy(human_hand_msgs__msg__SystemStatus * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    human_hand_msgs__msg__SystemStatus__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
human_hand_msgs__msg__SystemStatus__Sequence__init(human_hand_msgs__msg__SystemStatus__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__msg__SystemStatus * data = NULL;

  if (size) {
    data = (human_hand_msgs__msg__SystemStatus *)allocator.zero_allocate(size, sizeof(human_hand_msgs__msg__SystemStatus), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = human_hand_msgs__msg__SystemStatus__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        human_hand_msgs__msg__SystemStatus__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
human_hand_msgs__msg__SystemStatus__Sequence__fini(human_hand_msgs__msg__SystemStatus__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      human_hand_msgs__msg__SystemStatus__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

human_hand_msgs__msg__SystemStatus__Sequence *
human_hand_msgs__msg__SystemStatus__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__msg__SystemStatus__Sequence * array = (human_hand_msgs__msg__SystemStatus__Sequence *)allocator.allocate(sizeof(human_hand_msgs__msg__SystemStatus__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = human_hand_msgs__msg__SystemStatus__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
human_hand_msgs__msg__SystemStatus__Sequence__destroy(human_hand_msgs__msg__SystemStatus__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    human_hand_msgs__msg__SystemStatus__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
human_hand_msgs__msg__SystemStatus__Sequence__are_equal(const human_hand_msgs__msg__SystemStatus__Sequence * lhs, const human_hand_msgs__msg__SystemStatus__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!human_hand_msgs__msg__SystemStatus__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
human_hand_msgs__msg__SystemStatus__Sequence__copy(
  const human_hand_msgs__msg__SystemStatus__Sequence * input,
  human_hand_msgs__msg__SystemStatus__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(human_hand_msgs__msg__SystemStatus);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    human_hand_msgs__msg__SystemStatus * data =
      (human_hand_msgs__msg__SystemStatus *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!human_hand_msgs__msg__SystemStatus__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          human_hand_msgs__msg__SystemStatus__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!human_hand_msgs__msg__SystemStatus__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
