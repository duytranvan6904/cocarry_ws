// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice
#include "human_hand_msgs/msg/detail/hand_prediction__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `header`
#include "std_msgs/msg/detail/header__functions.h"
// Member `model_name`
#include "rosidl_runtime_c/string_functions.h"

bool
human_hand_msgs__msg__HandPrediction__init(human_hand_msgs__msg__HandPrediction * msg)
{
  if (!msg) {
    return false;
  }
  // header
  if (!std_msgs__msg__Header__init(&msg->header)) {
    human_hand_msgs__msg__HandPrediction__fini(msg);
    return false;
  }
  // x
  // y
  // z
  // inference_time_ms
  // model_name
  if (!rosidl_runtime_c__String__init(&msg->model_name)) {
    human_hand_msgs__msg__HandPrediction__fini(msg);
    return false;
  }
  // buffer_size
  // prediction_confidence
  return true;
}

void
human_hand_msgs__msg__HandPrediction__fini(human_hand_msgs__msg__HandPrediction * msg)
{
  if (!msg) {
    return;
  }
  // header
  std_msgs__msg__Header__fini(&msg->header);
  // x
  // y
  // z
  // inference_time_ms
  // model_name
  rosidl_runtime_c__String__fini(&msg->model_name);
  // buffer_size
  // prediction_confidence
}

bool
human_hand_msgs__msg__HandPrediction__are_equal(const human_hand_msgs__msg__HandPrediction * lhs, const human_hand_msgs__msg__HandPrediction * rhs)
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
  // x
  if (lhs->x != rhs->x) {
    return false;
  }
  // y
  if (lhs->y != rhs->y) {
    return false;
  }
  // z
  if (lhs->z != rhs->z) {
    return false;
  }
  // inference_time_ms
  if (lhs->inference_time_ms != rhs->inference_time_ms) {
    return false;
  }
  // model_name
  if (!rosidl_runtime_c__String__are_equal(
      &(lhs->model_name), &(rhs->model_name)))
  {
    return false;
  }
  // buffer_size
  if (lhs->buffer_size != rhs->buffer_size) {
    return false;
  }
  // prediction_confidence
  if (lhs->prediction_confidence != rhs->prediction_confidence) {
    return false;
  }
  return true;
}

bool
human_hand_msgs__msg__HandPrediction__copy(
  const human_hand_msgs__msg__HandPrediction * input,
  human_hand_msgs__msg__HandPrediction * output)
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
  // x
  output->x = input->x;
  // y
  output->y = input->y;
  // z
  output->z = input->z;
  // inference_time_ms
  output->inference_time_ms = input->inference_time_ms;
  // model_name
  if (!rosidl_runtime_c__String__copy(
      &(input->model_name), &(output->model_name)))
  {
    return false;
  }
  // buffer_size
  output->buffer_size = input->buffer_size;
  // prediction_confidence
  output->prediction_confidence = input->prediction_confidence;
  return true;
}

human_hand_msgs__msg__HandPrediction *
human_hand_msgs__msg__HandPrediction__create()
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__msg__HandPrediction * msg = (human_hand_msgs__msg__HandPrediction *)allocator.allocate(sizeof(human_hand_msgs__msg__HandPrediction), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(human_hand_msgs__msg__HandPrediction));
  bool success = human_hand_msgs__msg__HandPrediction__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
human_hand_msgs__msg__HandPrediction__destroy(human_hand_msgs__msg__HandPrediction * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    human_hand_msgs__msg__HandPrediction__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
human_hand_msgs__msg__HandPrediction__Sequence__init(human_hand_msgs__msg__HandPrediction__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__msg__HandPrediction * data = NULL;

  if (size) {
    data = (human_hand_msgs__msg__HandPrediction *)allocator.zero_allocate(size, sizeof(human_hand_msgs__msg__HandPrediction), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = human_hand_msgs__msg__HandPrediction__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        human_hand_msgs__msg__HandPrediction__fini(&data[i - 1]);
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
human_hand_msgs__msg__HandPrediction__Sequence__fini(human_hand_msgs__msg__HandPrediction__Sequence * array)
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
      human_hand_msgs__msg__HandPrediction__fini(&array->data[i]);
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

human_hand_msgs__msg__HandPrediction__Sequence *
human_hand_msgs__msg__HandPrediction__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  human_hand_msgs__msg__HandPrediction__Sequence * array = (human_hand_msgs__msg__HandPrediction__Sequence *)allocator.allocate(sizeof(human_hand_msgs__msg__HandPrediction__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = human_hand_msgs__msg__HandPrediction__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
human_hand_msgs__msg__HandPrediction__Sequence__destroy(human_hand_msgs__msg__HandPrediction__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    human_hand_msgs__msg__HandPrediction__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
human_hand_msgs__msg__HandPrediction__Sequence__are_equal(const human_hand_msgs__msg__HandPrediction__Sequence * lhs, const human_hand_msgs__msg__HandPrediction__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!human_hand_msgs__msg__HandPrediction__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
human_hand_msgs__msg__HandPrediction__Sequence__copy(
  const human_hand_msgs__msg__HandPrediction__Sequence * input,
  human_hand_msgs__msg__HandPrediction__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(human_hand_msgs__msg__HandPrediction);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    human_hand_msgs__msg__HandPrediction * data =
      (human_hand_msgs__msg__HandPrediction *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!human_hand_msgs__msg__HandPrediction__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          human_hand_msgs__msg__HandPrediction__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!human_hand_msgs__msg__HandPrediction__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
