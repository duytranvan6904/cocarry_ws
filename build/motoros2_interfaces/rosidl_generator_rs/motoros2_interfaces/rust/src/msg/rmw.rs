#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__AlarmInfo() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__AlarmInfo__init(msg: *mut AlarmInfo) -> bool;
    fn motoros2_interfaces__msg__AlarmInfo__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AlarmInfo>, size: usize) -> bool;
    fn motoros2_interfaces__msg__AlarmInfo__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AlarmInfo>);
    fn motoros2_interfaces__msg__AlarmInfo__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AlarmInfo>, out_seq: *mut rosidl_runtime_rs::Sequence<AlarmInfo>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__AlarmInfo
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlarmInfo {
    /// Alarm Number
    pub number: u32,

    /// Alarm Name/Message
    pub message: rosidl_runtime_rs::String,

    /// Sub Code
    pub sub_code: i32,

    /// reserved for future use
    ///
    /// Date & time at which this alarm was raised on the controller
    ///
    /// NOTE: in accordance with the "Clock and Time" ROS 2 design article, this
    /// stamp is in ROSTime == (local) SystemTime on Yaskawa Motoman robot
    /// controllers, as the latter is the only clock source supported on those
    /// platforms.
    ///
    /// This stamp will not be corrected for Host PC <-> Yaskawa controller clock
    /// drift, as it is intended purely for informational purposes (ie: for humans)
    /// at this time.
    pub datetime: builtin_interfaces::msg::rmw::Time,

    /// reserved for future use: contents (from CSV)
    pub contents: rosidl_runtime_rs::String,

    /// reserved for future use: meaning (from CSV)
    pub description: rosidl_runtime_rs::String,

    /// reserved for future use: potential causes and their potential remedies (from CSV)
    pub help: rosidl_runtime_rs::Sequence<super::super::msg::rmw::AlarmCauseRemedy>,

}



impl Default for AlarmInfo {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__AlarmInfo__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__AlarmInfo__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AlarmInfo {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__AlarmInfo__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__AlarmInfo__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__AlarmInfo__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AlarmInfo {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AlarmInfo where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/AlarmInfo";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__AlarmInfo() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__AlarmCauseRemedy() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__AlarmCauseRemedy__init(msg: *mut AlarmCauseRemedy) -> bool;
    fn motoros2_interfaces__msg__AlarmCauseRemedy__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<AlarmCauseRemedy>, size: usize) -> bool;
    fn motoros2_interfaces__msg__AlarmCauseRemedy__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<AlarmCauseRemedy>);
    fn motoros2_interfaces__msg__AlarmCauseRemedy__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<AlarmCauseRemedy>, out_seq: *mut rosidl_runtime_rs::Sequence<AlarmCauseRemedy>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__AlarmCauseRemedy
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlarmCauseRemedy {
    /// Cause
    pub cause: rosidl_runtime_rs::String,

    /// Remedy
    pub remedy: rosidl_runtime_rs::String,

}



impl Default for AlarmCauseRemedy {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__AlarmCauseRemedy__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__AlarmCauseRemedy__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for AlarmCauseRemedy {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__AlarmCauseRemedy__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__AlarmCauseRemedy__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__AlarmCauseRemedy__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for AlarmCauseRemedy {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for AlarmCauseRemedy where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/AlarmCauseRemedy";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__AlarmCauseRemedy() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__ErrorInfo() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__ErrorInfo__init(msg: *mut ErrorInfo) -> bool;
    fn motoros2_interfaces__msg__ErrorInfo__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ErrorInfo>, size: usize) -> bool;
    fn motoros2_interfaces__msg__ErrorInfo__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ErrorInfo>);
    fn motoros2_interfaces__msg__ErrorInfo__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ErrorInfo>, out_seq: *mut rosidl_runtime_rs::Sequence<ErrorInfo>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__ErrorInfo
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ErrorInfo {
    /// Error Number
    pub number: u32,

    /// Error Name/Message
    pub message: rosidl_runtime_rs::String,

    /// Sub Code
    pub sub_code: i32,

    /// reserved for future use
    ///
    /// Date & time at which this error was raised on the controller
    ///
    /// NOTE: in accordance with the "Clock and Time" ROS 2 design article, this
    /// stamp is in ROSTime == (local) SystemTime on Yaskawa Motoman robot
    /// controllers, as the latter is the only clock source supported on those
    /// platforms.
    ///
    /// This stamp will not be corrected for Host PC <-> Yaskawa controller clock
    /// drift, as it is intended purely for informational purposes (ie: for humans)
    /// at this time.
    pub datetime: builtin_interfaces::msg::rmw::Time,

}



impl Default for ErrorInfo {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__ErrorInfo__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__ErrorInfo__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ErrorInfo {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__ErrorInfo__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__ErrorInfo__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__ErrorInfo__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ErrorInfo {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ErrorInfo where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/ErrorInfo";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__ErrorInfo() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__InformJobCrudResultCodes() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__InformJobCrudResultCodes__init(msg: *mut InformJobCrudResultCodes) -> bool;
    fn motoros2_interfaces__msg__InformJobCrudResultCodes__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<InformJobCrudResultCodes>, size: usize) -> bool;
    fn motoros2_interfaces__msg__InformJobCrudResultCodes__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<InformJobCrudResultCodes>);
    fn motoros2_interfaces__msg__InformJobCrudResultCodes__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<InformJobCrudResultCodes>, out_seq: *mut rosidl_runtime_rs::Sequence<InformJobCrudResultCodes>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__InformJobCrudResultCodes
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2024, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2024, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct InformJobCrudResultCodes {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}

impl InformJobCrudResultCodes {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RC_OK: u32 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STR_OK: &'static str = "Success";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RC_ERR_REFRESHING_JOB_LIST: u32 = 10;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STR_ERR_REFRESHING_JOB_LIST: &'static str = "Error refreshing job list";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RC_ERR_RETRIEVING_FILE_COUNT: u32 = 11;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STR_ERR_RETRIEVING_FILE_COUNT: &'static str = "Error retrieving file count";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RC_ERR_TOO_MANY_JOBS: u32 = 12;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STR_ERR_TOO_MANY_JOBS: &'static str = "Too many jobs";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RC_ERR_RETRIEVING_JOB_NAME_FROM_LIST: u32 = 13;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STR_ERR_RETRIEVING_JOB_NAME_FROM_LIST: &'static str = "Failed retrieving job name from list";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const RC_ERR_APPENDING_JOB_NAME_TO_SVC_RESPONSE: u32 = 14;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const STR_ERR_APPENDING_JOB_NAME_TO_SVC_RESPONSE: &'static str = "Error adding job name to service response";

}


impl Default for InformJobCrudResultCodes {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__InformJobCrudResultCodes__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__InformJobCrudResultCodes__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for InformJobCrudResultCodes {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__InformJobCrudResultCodes__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__InformJobCrudResultCodes__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__InformJobCrudResultCodes__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for InformJobCrudResultCodes {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for InformJobCrudResultCodes where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/InformJobCrudResultCodes";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__InformJobCrudResultCodes() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__InitTrajEnum() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__InitTrajEnum__init(msg: *mut InitTrajEnum) -> bool;
    fn motoros2_interfaces__msg__InitTrajEnum__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<InitTrajEnum>, size: usize) -> bool;
    fn motoros2_interfaces__msg__InitTrajEnum__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<InitTrajEnum>);
    fn motoros2_interfaces__msg__InitTrajEnum__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<InitTrajEnum>, out_seq: *mut rosidl_runtime_rs::Sequence<InitTrajEnum>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__InitTrajEnum
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2024, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2024, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct InitTrajEnum {

    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u16,

}

impl InitTrajEnum {
    /// Result codes which may be returned when attempting to initialize trajectory
    ///
    /// Values other than 0 would indicate an active error or other active inhibition
    /// on the Yaskawa controller preventing MotoROS2 from initializing a trajectory
    ///
    /// Applications are encouraged to refer to the named constants generated by
    /// rosidl as part of this message instead of using the integer values directly.
    pub const INIT_TRAJ_OK: u16 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_OK_STR: &'static str = "OK";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_UNSPECIFIED: u16 = 200;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_UNSPECIFIED_STR: &'static str = "Unspecified failure";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_TOO_SMALL: u16 = 201;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_TOO_SMALL_STR: &'static str = "Trajectory must contain at least two points.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_TOO_BIG: u16 = 202;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_TOO_BIG_STR: &'static str = "Trajectory contains too many points (Not enough memory).";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_ALREADY_IN_MOTION: u16 = 203;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_ALREADY_IN_MOTION_STR: &'static str = "Already running a trajectory.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_STARTING_POS: u16 = 204;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_STARTING_POS_STR: &'static str = "The first point must match the robot\'s current position.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_VELOCITY: u16 = 205;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_VELOCITY_STR: &'static str = "The commanded velocity is too high.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_JOINTNAME: u16 = 206;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_JOINTNAME_STR: &'static str = "Invalid joint name specified. Check motoros2_config.yaml.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INCOMPLETE_JOINTLIST: u16 = 207;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INCOMPLETE_JOINTLIST_STR: &'static str = "Trajectory must contain data for all joints.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_TIME: u16 = 208;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_TIME_STR: &'static str = "Invalid time in trajectory.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_WRONG_MODE: u16 = 209;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_WRONG_MODE_STR: &'static str = "Must call start_traj_mode service";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_BACKWARD_TIME: u16 = 210;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_BACKWARD_TIME_STR: &'static str = "Trajectory message contains waypoints that are not strictly increasing in time.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS: u16 = 211;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR: &'static str = "Trajectory did not contain position data for all axes.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES: u16 = 212;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR: &'static str = "Trajectory did not contain velocity data for all axes.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_ENDING_VELOCITY: u16 = 213;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_ENDING_VELOCITY_STR: &'static str = "The final point in the trajectory must have zero velocity.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_ENDING_ACCELERATION: u16 = 214;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR: &'static str = "The final point in the trajectory must have zero acceleration.";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_DUPLICATE_JOINT_NAME: u16 = 215;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_TRAJ_DUPLICATE_JOINT_NAME_STR: &'static str = "The trajectory contains duplicate joint names.";

}


impl Default for InitTrajEnum {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__InitTrajEnum__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__InitTrajEnum__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for InitTrajEnum {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__InitTrajEnum__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__InitTrajEnum__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__InitTrajEnum__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for InitTrajEnum {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for InitTrajEnum where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/InitTrajEnum";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__InitTrajEnum() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__IoResultCodes() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__IoResultCodes__init(msg: *mut IoResultCodes) -> bool;
    fn motoros2_interfaces__msg__IoResultCodes__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<IoResultCodes>, size: usize) -> bool;
    fn motoros2_interfaces__msg__IoResultCodes__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<IoResultCodes>);
    fn motoros2_interfaces__msg__IoResultCodes__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<IoResultCodes>, out_seq: *mut rosidl_runtime_rs::Sequence<IoResultCodes>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__IoResultCodes
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct IoResultCodes {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}

impl IoResultCodes {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const OK: u32 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const OK_STR: &'static str = "Success";

    /// The ioAddress cannot be read on this controller
    pub const READ_ADDRESS_INVALID: u32 = 1001;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READ_ADDRESS_INVALID_STR: &'static str = "Address cannot be read from (out of readable range)";

    /// The ioAddress cannot be written to on this controller
    pub const WRITE_ADDRESS_INVALID: u32 = 1002;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const WRITE_ADDRESS_INVALID_STR: &'static str = "Address cannot be written to (out of writable range)";

    /// The value supplied is not a valid value for the addressed IO element
    pub const WRITE_VALUE_INVALID: u32 = 1003;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const WRITE_VALUE_INVALID_STR: &'static str = "Illegal value for the type of IO element addressed";

    /// mpReadIO return -1
    pub const READ_API_ERROR: u32 = 1004;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READ_API_ERROR_STR: &'static str = "The MotoPlus function mpReadIO returned -1. No further information is available";

    /// mpWriteIO returned -1
    pub const WRITE_API_ERROR: u32 = 1005;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const WRITE_API_ERROR_STR: &'static str = "The MotoPlus function mpWriteIO returned -1. No further information is available";

    /// Unknown fallback failure
    pub const UNKNOWN_API_ERROR_STR: &'static str = "Unknown error accessing I/O. No further information is available";

}


impl Default for IoResultCodes {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__IoResultCodes__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__IoResultCodes__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for IoResultCodes {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__IoResultCodes__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__IoResultCodes__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__IoResultCodes__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for IoResultCodes {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for IoResultCodes where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/IoResultCodes";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__IoResultCodes() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__MotionReadyEnum() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__MotionReadyEnum__init(msg: *mut MotionReadyEnum) -> bool;
    fn motoros2_interfaces__msg__MotionReadyEnum__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<MotionReadyEnum>, size: usize) -> bool;
    fn motoros2_interfaces__msg__MotionReadyEnum__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<MotionReadyEnum>);
    fn motoros2_interfaces__msg__MotionReadyEnum__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<MotionReadyEnum>, out_seq: *mut rosidl_runtime_rs::Sequence<MotionReadyEnum>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__MotionReadyEnum
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct MotionReadyEnum {

    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u16,

}

impl MotionReadyEnum {
    /// Result codes which may be returned by services and actions which attempt to
    /// execute motion (or are executing motion).
    ///
    /// Values other than 1 would indicate an active error or other active inhibition
    /// on the Yaskawa controller preventing MotoROS2 from enabling trajectory mode
    /// or executing any motion.
    ///
    /// Applications are encouraged to refer to the named constants generated by
    /// rosidl as part of this message instead of using the integer values directly.
    pub const READY: u16 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const READY_STR: &'static str = "Ready";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_UNSPECIFIED: u16 = 100;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_UNSPECIFIED_STR: &'static str = "Unspecified";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ALARM: u16 = 101;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ALARM_STR: &'static str = "The controller has an active Alarm";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ERROR: u16 = 102;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ERROR_STR: &'static str = "The controller has an active Error";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ESTOP: u16 = 103;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ESTOP_STR: &'static str = "The controller is in E-Stop";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_PLAY: u16 = 104;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_PLAY_STR: &'static str = "The teach pendant must not be in TEACH mode";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_REMOTE: u16 = 105;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_REMOTE_STR: &'static str = "The teach pendant must be in REMOTE mode";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_SERVO_OFF: u16 = 106;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_SERVO_OFF_STR: &'static str = "Servo power is OFF. Please call start_traj_mode or start_point_queue_mode service";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_HOLD: u16 = 107;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_HOLD_STR: &'static str = "The controller is in HOLD";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_JOB_NOT_STARTED: u16 = 108;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_JOB_NOT_STARTED_STR: &'static str = "The INIT_ROS job has not started. Please call start_traj_mode or start_point_queue_mode service";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_ON_WAIT_CMD: u16 = 109;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_ON_WAIT_CMD_STR: &'static str = "INFORM job is not on a WAIT command. Check the format of INIT_ROS";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_PFL_ACTIVE: u16 = 111;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_PFL_ACTIVE_STR: &'static str = "A PFL event has occurred. Please return the robot to a safe state";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_INC_MOVE_ERROR: u16 = 112;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_INC_MOVE_ERROR_STR: &'static str = "The controller is in an error state. Please call reset_error to attempt to clear the error";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_OTHER_PROGRAM_RUNNING: u16 = 113;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_OTHER_PROGRAM_RUNNING_STR: &'static str = "Controller is running another job";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_OTHER_TRAJ_MODE_ACTIVE: u16 = 114;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_OTHER_TRAJ_MODE_ACTIVE_STR: &'static str = "Another trajectory mode is already active. Please call stop_traj_mode service";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_CONT_CYCLE_MODE: u16 = 115;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_NOT_CONT_CYCLE_MODE_STR: &'static str = "AUTO cycle mode not set. Please set the cycle mode to AUTO";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_MAJOR_ALARM: u16 = 116;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_MAJOR_ALARM_STR: &'static str = "Major Alarms can\'t be reset. Please check the teach pendant";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ECO_MODE: u16 = 117;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_ECO_MODE_STR: &'static str = "Couldn\'t disable eco mode";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_SERVO_ON_TIMEOUT: u16 = 118;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NOT_READY_SERVO_ON_TIMEOUT_STR: &'static str = "Timed out while waiting for servo on";

}


impl Default for MotionReadyEnum {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__MotionReadyEnum__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__MotionReadyEnum__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for MotionReadyEnum {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__MotionReadyEnum__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__MotionReadyEnum__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__MotionReadyEnum__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for MotionReadyEnum {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for MotionReadyEnum where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/MotionReadyEnum";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__MotionReadyEnum() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__QueueResultEnum() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__QueueResultEnum__init(msg: *mut QueueResultEnum) -> bool;
    fn motoros2_interfaces__msg__QueueResultEnum__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<QueueResultEnum>, size: usize) -> bool;
    fn motoros2_interfaces__msg__QueueResultEnum__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<QueueResultEnum>);
    fn motoros2_interfaces__msg__QueueResultEnum__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<QueueResultEnum>, out_seq: *mut rosidl_runtime_rs::Sequence<QueueResultEnum>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__QueueResultEnum
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QueueResultEnum {

    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u16,

}

impl QueueResultEnum {
    /// The result code for an attempted invocation of the queue_traj_point service
    pub const SUCCESS: u16 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SUCCESS_STR: &'static str = "";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const WRONG_MODE: u16 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const WRONG_MODE_STR: &'static str = "Must call start_point_queue_mode service";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_FAILURE: u16 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INIT_FAILURE_STR: &'static str = "Failed to initialize the streaming trajectory";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const BUSY: u16 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const BUSY_STR: &'static str = "Busy processing the previous trajectory point. Please resend the next point shortly";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_JOINT_LIST: u16 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_JOINT_LIST_STR: &'static str = "Point must contain data for all joints";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const UNABLE_TO_PROCESS_POINT: u16 = 6;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const UNABLE_TO_PROCESS_POINT_STR: &'static str = "Error while processing the trajectory point. Check debug log for more details";

}


impl Default for QueueResultEnum {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__QueueResultEnum__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__QueueResultEnum__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for QueueResultEnum {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__QueueResultEnum__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__QueueResultEnum__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__QueueResultEnum__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for QueueResultEnum {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for QueueResultEnum where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/QueueResultEnum";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__QueueResultEnum() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__SelectionResultCodes() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__msg__SelectionResultCodes__init(msg: *mut SelectionResultCodes) -> bool;
    fn motoros2_interfaces__msg__SelectionResultCodes__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SelectionResultCodes>, size: usize) -> bool;
    fn motoros2_interfaces__msg__SelectionResultCodes__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SelectionResultCodes>);
    fn motoros2_interfaces__msg__SelectionResultCodes__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SelectionResultCodes>, out_seq: *mut rosidl_runtime_rs::Sequence<SelectionResultCodes>) -> bool;
}

// Corresponds to motoros2_interfaces__msg__SelectionResultCodes
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectionResultCodes {

    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u32,

}

impl SelectionResultCodes {
    /// Result codes which may be returned by services and actions which attempt to
    /// select a configuration or setting.
    ///
    /// Values other than 0 would indicate an active error or other active inhibition
    /// on the Yaskawa controller preventing MotoROS2 from processing the service
    /// request.
    ///
    /// Applications are encouraged to refer to the named constants generated by
    /// rosidl as part of this message instead of using the integer values directly.
    pub const OK: u32 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const OK_STR: &'static str = "";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_CONTROLLER_STATE: u32 = 400;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_CONTROLLER_STATE_STR: &'static str = "Pendant is not in REMOTE mode";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_CONTROL_GROUP: u32 = 401;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_CONTROL_GROUP_STR: &'static str = "Invalid control group";


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_SELECTION_INDEX: u32 = 402;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INVALID_SELECTION_INDEX_STR: &'static str = "Invalid tool selection";

}


impl Default for SelectionResultCodes {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__msg__SelectionResultCodes__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__msg__SelectionResultCodes__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SelectionResultCodes {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__SelectionResultCodes__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__SelectionResultCodes__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__msg__SelectionResultCodes__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SelectionResultCodes {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SelectionResultCodes where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/msg/SelectionResultCodes";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__msg__SelectionResultCodes() }
  }
}


