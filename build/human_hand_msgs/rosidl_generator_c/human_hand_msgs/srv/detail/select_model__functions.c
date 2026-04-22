// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from human_hand_msgs:srv/SelectModel.idl
// generated code does not contain a copyright notice
#include "human_hand_msgs/srv/detail/select_model__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"

// Include directives for member types
// Member `model_name`
#include "rosidl_runtime_c/string_functions.h"

bool
human_hand_msgs__srv__SelectModel_Request__init(human_hand_msgs__srv__SelectModel_Request * msg)
{
  if (!msg) {
    return false;
  }
  // model_name
  if (!rosidl_runtime_c__String__init(&msg->model_name)) {
    human_hand_msgs__srv__SelectModel_Request__fini(msg);
    return false;
  }
  return true;
}

void
human_hand_msgs__srv__SelectModel_Request__fini(human_hand_msgs__srv__SelectModel_Request * msg)
{
  if (!msg) {
    return;
  }
  // model_name
  rosidl_runtime_c__String__fini(&msg->model_name);
}

bool
human_hand_msgs__srv__SelectModel_Request__are_equal(const human_hand_msgs__srv__SelectModel_Request * lhs, const human_hand_msgs__srv__SelectModel_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // model_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->model_name), &(rhs->model_name)))
  {
    return false;
  }
  return true;
}

bool
human_hand_msgs__srv__SelectModel_Request__copy(
  const human_hand_msgs__srv__SelectModel_Request * input,
  human_hand_msgs__srv__SelectModel_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // model_name
  if (!rosidl_runtime_c__String__copy(
      &(input->model_name), &(output->model_name)))
  {
    return false;
  }
  return true;
}

human_hand_msgs__srv__SelectModel_Request *
human_hand_msgs__srv__SelectModel_Request__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__srv__SelectModel_Request * msg = (human_hand_msgs__srv__SelectModel_Request *)allocator.allocate(sizeof(human_hand_msgs__srv__SelectModel_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(human_hand_msgs__srv__SelectModel_Request));
  bool success = human_hand_msgs__srv__SelectModel_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
human_hand_msgs__srv__SelectModel_Request__destroy(human_hand_msgs__srv__SelectModel_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    human_hand_msgs__srv__SelectModel_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
human_hand_msgs__srv__SelectModel_Request__Sequence__init(human_hand_msgs__srv__SelectModel_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__srv__SelectModel_Request * data = NULL;

  if (size) {
    data = (human_hand_msgs__srv__SelectModel_Request *)allocator.zero_allocate(size, sizeof(human_hand_msgs__srv__SelectModel_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = human_hand_msgs__srv__SelectModel_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        human_hand_msgs__srv__SelectModel_Request__fini(&data[i - 1]);
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
human_hand_msgs__srv__SelectModel_Request__Sequence__fini(human_hand_msgs__srv__SelectModel_Request__Sequence * array)
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
      human_hand_msgs__srv__SelectModel_Request__fini(&array->data[i]);
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

human_hand_msgs__srv__SelectModel_Request__Sequence *
human_hand_msgs__srv__SelectModel_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__srv__SelectModel_Request__Sequence * array = (human_hand_msgs__srv__SelectModel_Request__Sequence *)allocator.allocate(sizeof(human_hand_msgs__srv__SelectModel_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = human_hand_msgs__srv__SelectModel_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
human_hand_msgs__srv__SelectModel_Request__Sequence__destroy(human_hand_msgs__srv__SelectModel_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    human_hand_msgs__srv__SelectModel_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
human_hand_msgs__srv__SelectModel_Request__Sequence__are_equal(const human_hand_msgs__srv__SelectModel_Request__Sequence * lhs, const human_hand_msgs__srv__SelectModel_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!human_hand_msgs__srv__SelectModel_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
human_hand_msgs__srv__SelectModel_Request__Sequence__copy(
  const human_hand_msgs__srv__SelectModel_Request__Sequence * input,
  human_hand_msgs__srv__SelectModel_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(human_hand_msgs__srv__SelectModel_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    human_hand_msgs__srv__SelectModel_Request * data =
      (human_hand_msgs__srv__SelectModel_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!human_hand_msgs__srv__SelectModel_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          human_hand_msgs__srv__SelectModel_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!human_hand_msgs__srv__SelectModel_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `message`
// Member `active_model`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
human_hand_msgs__srv__SelectModel_Response__init(human_hand_msgs__srv__SelectModel_Response * msg)
{
  if (!msg) {
    return false;
  }
  // success
  // message
  if (!rosidl_runtime_c__String__init(&msg->message)) {
    human_hand_msgs__srv__SelectModel_Response__fini(msg);
    return false;
  }
  // active_model
  if (!rosidl_runtime_c__String__init(&msg->active_model)) {
    human_hand_msgs__srv__SelectModel_Response__fini(msg);
    return false;
  }
  return true;
}

void
human_hand_msgs__srv__SelectModel_Response__fini(human_hand_msgs__srv__SelectModel_Response * msg)
{
  if (!msg) {
    return;
  }
  // success
  // message
  rosidl_runtime_c__String__fini(&msg->message);
  // active_model
  rosidl_runtime_c__String__fini(&msg->active_model);
}

bool
human_hand_msgs__srv__SelectModel_Response__are_equal(const human_hand_msgs__srv__SelectModel_Response * lhs, const human_hand_msgs__srv__SelectModel_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // success
  if (lhs->success != rhs->success) {
    return false;
  }
  // message
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->message), &(rhs->message)))
  {
    return false;
  }
  // active_model
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->active_model), &(rhs->active_model)))
  {
    return false;
  }
  return true;
}

bool
human_hand_msgs__srv__SelectModel_Response__copy(
  const human_hand_msgs__srv__SelectModel_Response * input,
  human_hand_msgs__srv__SelectModel_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // success
  output->success = input->success;
  // message
  if (!rosidl_runtime_c__String__copy(
      &(input->message), &(output->message)))
  {
    return false;
  }
  // active_model
  if (!rosidl_runtime_c__String__copy(
      &(input->active_model), &(output->active_model)))
  {
    return false;
  }
  return true;
}

human_hand_msgs__srv__SelectModel_Response *
human_hand_msgs__srv__SelectModel_Response__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__srv__SelectModel_Response * msg = (human_hand_msgs__srv__SelectModel_Response *)allocator.allocate(sizeof(human_hand_msgs__srv__SelectModel_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(human_hand_msgs__srv__SelectModel_Response));
  bool success = human_hand_msgs__srv__SelectModel_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
human_hand_msgs__srv__SelectModel_Response__destroy(human_hand_msgs__srv__SelectModel_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    human_hand_msgs__srv__SelectModel_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
human_hand_msgs__srv__SelectModel_Response__Sequence__init(human_hand_msgs__srv__SelectModel_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__srv__SelectModel_Response * data = NULL;

  if (size) {
    data = (human_hand_msgs__srv__SelectModel_Response *)allocator.zero_allocate(size, sizeof(human_hand_msgs__srv__SelectModel_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = human_hand_msgs__srv__SelectModel_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        human_hand_msgs__srv__SelectModel_Response__fini(&data[i - 1]);
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
human_hand_msgs__srv__SelectModel_Response__Sequence__fini(human_hand_msgs__srv__SelectModel_Response__Sequence * array)
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
      human_hand_msgs__srv__SelectModel_Response__fini(&array->data[i]);
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

human_hand_msgs__srv__SelectModel_Response__Sequence *
human_hand_msgs__srv__SelectModel_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__srv__SelectModel_Response__Sequence * array = (human_hand_msgs__srv__SelectModel_Response__Sequence *)allocator.allocate(sizeof(human_hand_msgs__srv__SelectModel_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = human_hand_msgs__srv__SelectModel_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
human_hand_msgs__srv__SelectModel_Response__Sequence__destroy(human_hand_msgs__srv__SelectModel_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    human_hand_msgs__srv__SelectModel_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
human_hand_msgs__srv__SelectModel_Response__Sequence__are_equal(const human_hand_msgs__srv__SelectModel_Response__Sequence * lhs, const human_hand_msgs__srv__SelectModel_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!human_hand_msgs__srv__SelectModel_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
human_hand_msgs__srv__SelectModel_Response__Sequence__copy(
  const human_hand_msgs__srv__SelectModel_Response__Sequence * input,
  human_hand_msgs__srv__SelectModel_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(human_hand_msgs__srv__SelectModel_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    human_hand_msgs__srv__SelectModel_Response * data =
      (human_hand_msgs__srv__SelectModel_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!human_hand_msgs__srv__SelectModel_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          human_hand_msgs__srv__SelectModel_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!human_hand_msgs__srv__SelectModel_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
