// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from human_hand_msgs:msg/HandPrediction.idl
// generated code does not contain a copyright notice

#ifndef HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__FUNCTIONS_H_
#define HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "human_hand_msgs/msg/rosidl_generator_c__visibility_control.h"

#include "human_hand_msgs/msg/detail/hand_prediction__struct.h"

/// Initialize msg/HandPrediction message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * human_hand_msgs__msg__HandPrediction
 * )) before or use
 * human_hand_msgs__msg__HandPrediction__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
bool
human_hand_msgs__msg__HandPrediction__init(human_hand_msgs__msg__HandPrediction * msg);

/// Finalize msg/HandPrediction message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
void
human_hand_msgs__msg__HandPrediction__fini(human_hand_msgs__msg__HandPrediction * msg);

/// Create msg/HandPrediction message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * human_hand_msgs__msg__HandPrediction__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
human_hand_msgs__msg__HandPrediction *
human_hand_msgs__msg__HandPrediction__create();

/// Destroy msg/HandPrediction message.
/**
 * It calls
 * human_hand_msgs__msg__HandPrediction__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
void
human_hand_msgs__msg__HandPrediction__destroy(human_hand_msgs__msg__HandPrediction * msg);

/// Check for msg/HandPrediction message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
bool
human_hand_msgs__msg__HandPrediction__are_equal(const human_hand_msgs__msg__HandPrediction * lhs, const human_hand_msgs__msg__HandPrediction * rhs);

/// Copy a msg/HandPrediction message.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source message pointer.
 * \param[out] output The target message pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer is null
 *   or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
bool
human_hand_msgs__msg__HandPrediction__copy(
  const human_hand_msgs__msg__HandPrediction * input,
  human_hand_msgs__msg__HandPrediction * output);

/// Initialize array of msg/HandPrediction messages.
/**
 * It allocates the memory for the number of elements and calls
 * human_hand_msgs__msg__HandPrediction__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
bool
human_hand_msgs__msg__HandPrediction__Sequence__init(human_hand_msgs__msg__HandPrediction__Sequence * array, size_t size);

/// Finalize array of msg/HandPrediction messages.
/**
 * It calls
 * human_hand_msgs__msg__HandPrediction__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
void
human_hand_msgs__msg__HandPrediction__Sequence__fini(human_hand_msgs__msg__HandPrediction__Sequence * array);

/// Create array of msg/HandPrediction messages.
/**
 * It allocates the memory for the array and calls
 * human_hand_msgs__msg__HandPrediction__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
human_hand_msgs__msg__HandPrediction__Sequence *
human_hand_msgs__msg__HandPrediction__Sequence__create(size_t size);

/// Destroy array of msg/HandPrediction messages.
/**
 * It calls
 * human_hand_msgs__msg__HandPrediction__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
void
human_hand_msgs__msg__HandPrediction__Sequence__destroy(human_hand_msgs__msg__HandPrediction__Sequence * array);

/// Check for msg/HandPrediction message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
bool
human_hand_msgs__msg__HandPrediction__Sequence__are_equal(const human_hand_msgs__msg__HandPrediction__Sequence * lhs, const human_hand_msgs__msg__HandPrediction__Sequence * rhs);

/// Copy an array of msg/HandPrediction messages.
/**
 * This functions performs a deep copy, as opposed to the shallow copy that
 * plain assignment yields.
 *
 * \param[in] input The source array pointer.
 * \param[out] output The target array pointer, which must
 *   have been initialized before calling this function.
 * \return true if successful, or false if either pointer
 *   is null or memory allocation fails.
 */
ROSIDL_GENERATOR_C_PUBLIC_human_hand_msgs
bool
human_hand_msgs__msg__HandPrediction__Sequence__copy(
  const human_hand_msgs__msg__HandPrediction__Sequence * input,
  human_hand_msgs__msg__HandPrediction__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // HUMAN_HAND_MSGS__MSG__DETAIL__HAND_PREDICTION__FUNCTIONS_H_
