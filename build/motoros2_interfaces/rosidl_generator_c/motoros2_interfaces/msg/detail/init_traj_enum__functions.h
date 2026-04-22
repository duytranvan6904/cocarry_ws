// generated from rosidl_generator_c/resource/idl__functions.h.em
// with input from motoros2_interfaces:msg/InitTrajEnum.idl
// generated code does not contain a copyright notice

#ifndef MOTOROS2_INTERFACES__MSG__DETAIL__INIT_TRAJ_ENUM__FUNCTIONS_H_
#define MOTOROS2_INTERFACES__MSG__DETAIL__INIT_TRAJ_ENUM__FUNCTIONS_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stdlib.h>

#include "rosidl_runtime_c/visibility_control.h"
#include "motoros2_interfaces/msg/rosidl_generator_c__visibility_control.h"

#include "motoros2_interfaces/msg/detail/init_traj_enum__struct.h"

/// Initialize msg/InitTrajEnum message.
/**
 * If the init function is called twice for the same message without
 * calling fini inbetween previously allocated memory will be leaked.
 * \param[in,out] msg The previously allocated message pointer.
 * Fields without a default value will not be initialized by this function.
 * You might want to call memset(msg, 0, sizeof(
 * motoros2_interfaces__msg__InitTrajEnum
 * )) before or use
 * motoros2_interfaces__msg__InitTrajEnum__create()
 * to allocate and initialize the message.
 * \return true if initialization was successful, otherwise false
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
bool
motoros2_interfaces__msg__InitTrajEnum__init(motoros2_interfaces__msg__InitTrajEnum * msg);

/// Finalize msg/InitTrajEnum message.
/**
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
void
motoros2_interfaces__msg__InitTrajEnum__fini(motoros2_interfaces__msg__InitTrajEnum * msg);

/// Create msg/InitTrajEnum message.
/**
 * It allocates the memory for the message, sets the memory to zero, and
 * calls
 * motoros2_interfaces__msg__InitTrajEnum__init().
 * \return The pointer to the initialized message if successful,
 * otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
motoros2_interfaces__msg__InitTrajEnum *
motoros2_interfaces__msg__InitTrajEnum__create();

/// Destroy msg/InitTrajEnum message.
/**
 * It calls
 * motoros2_interfaces__msg__InitTrajEnum__fini()
 * and frees the memory of the message.
 * \param[in,out] msg The allocated message pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
void
motoros2_interfaces__msg__InitTrajEnum__destroy(motoros2_interfaces__msg__InitTrajEnum * msg);

/// Check for msg/InitTrajEnum message equality.
/**
 * \param[in] lhs The message on the left hand size of the equality operator.
 * \param[in] rhs The message on the right hand size of the equality operator.
 * \return true if messages are equal, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
bool
motoros2_interfaces__msg__InitTrajEnum__are_equal(const motoros2_interfaces__msg__InitTrajEnum * lhs, const motoros2_interfaces__msg__InitTrajEnum * rhs);

/// Copy a msg/InitTrajEnum message.
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
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
bool
motoros2_interfaces__msg__InitTrajEnum__copy(
  const motoros2_interfaces__msg__InitTrajEnum * input,
  motoros2_interfaces__msg__InitTrajEnum * output);

/// Initialize array of msg/InitTrajEnum messages.
/**
 * It allocates the memory for the number of elements and calls
 * motoros2_interfaces__msg__InitTrajEnum__init()
 * for each element of the array.
 * \param[in,out] array The allocated array pointer.
 * \param[in] size The size / capacity of the array.
 * \return true if initialization was successful, otherwise false
 * If the array pointer is valid and the size is zero it is guaranteed
 # to return true.
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
bool
motoros2_interfaces__msg__InitTrajEnum__Sequence__init(motoros2_interfaces__msg__InitTrajEnum__Sequence * array, size_t size);

/// Finalize array of msg/InitTrajEnum messages.
/**
 * It calls
 * motoros2_interfaces__msg__InitTrajEnum__fini()
 * for each element of the array and frees the memory for the number of
 * elements.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
void
motoros2_interfaces__msg__InitTrajEnum__Sequence__fini(motoros2_interfaces__msg__InitTrajEnum__Sequence * array);

/// Create array of msg/InitTrajEnum messages.
/**
 * It allocates the memory for the array and calls
 * motoros2_interfaces__msg__InitTrajEnum__Sequence__init().
 * \param[in] size The size / capacity of the array.
 * \return The pointer to the initialized array if successful, otherwise NULL
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
motoros2_interfaces__msg__InitTrajEnum__Sequence *
motoros2_interfaces__msg__InitTrajEnum__Sequence__create(size_t size);

/// Destroy array of msg/InitTrajEnum messages.
/**
 * It calls
 * motoros2_interfaces__msg__InitTrajEnum__Sequence__fini()
 * on the array,
 * and frees the memory of the array.
 * \param[in,out] array The initialized array pointer.
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
void
motoros2_interfaces__msg__InitTrajEnum__Sequence__destroy(motoros2_interfaces__msg__InitTrajEnum__Sequence * array);

/// Check for msg/InitTrajEnum message array equality.
/**
 * \param[in] lhs The message array on the left hand size of the equality operator.
 * \param[in] rhs The message array on the right hand size of the equality operator.
 * \return true if message arrays are equal in size and content, otherwise false.
 */
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
bool
motoros2_interfaces__msg__InitTrajEnum__Sequence__are_equal(const motoros2_interfaces__msg__InitTrajEnum__Sequence * lhs, const motoros2_interfaces__msg__InitTrajEnum__Sequence * rhs);

/// Copy an array of msg/InitTrajEnum messages.
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
ROSIDL_GENERATOR_C_PUBLIC_motoros2_interfaces
bool
motoros2_interfaces__msg__InitTrajEnum__Sequence__copy(
  const motoros2_interfaces__msg__InitTrajEnum__Sequence * input,
  motoros2_interfaces__msg__InitTrajEnum__Sequence * output);

#ifdef __cplusplus
}
#endif

#endif  // MOTOROS2_INTERFACES__MSG__DETAIL__INIT_TRAJ_ENUM__FUNCTIONS_H_
