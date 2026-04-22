#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "industrial_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__DebugLevel() -> *const std::ffi::c_void;
}

#[link(name = "industrial_msgs__rosidl_generator_c")]
extern "C" {
    fn industrial_msgs__msg__DebugLevel__init(msg: *mut DebugLevel) -> bool;
    fn industrial_msgs__msg__DebugLevel__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DebugLevel>, size: usize) -> bool;
    fn industrial_msgs__msg__DebugLevel__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DebugLevel>);
    fn industrial_msgs__msg__DebugLevel__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DebugLevel>, out_seq: *mut rosidl_runtime_rs::Sequence<DebugLevel>) -> bool;
}

// Corresponds to industrial_msgs__msg__DebugLevel
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Debug level message enumeration.  This may replicate some functionality that
/// alreay exists in the ROS logger.
/// TODO: Get more information on the ROS Logger.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DebugLevel {

    // This member is not documented.
    #[allow(missing_docs)]
    pub val: u8,

}

impl DebugLevel {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const DEBUG: u8 = 5;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const INFO: u8 = 4;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const WARN: u8 = 3;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ERROR: u8 = 2;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FATAL: u8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const NONE: u8 = 0;

}


impl Default for DebugLevel {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !industrial_msgs__msg__DebugLevel__init(&mut msg as *mut _) {
        panic!("Call to industrial_msgs__msg__DebugLevel__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DebugLevel {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__DebugLevel__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__DebugLevel__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__DebugLevel__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DebugLevel {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DebugLevel where Self: Sized {
  const TYPE_NAME: &'static str = "industrial_msgs/msg/DebugLevel";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__DebugLevel() }
  }
}


#[link(name = "industrial_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__DeviceInfo() -> *const std::ffi::c_void;
}

#[link(name = "industrial_msgs__rosidl_generator_c")]
extern "C" {
    fn industrial_msgs__msg__DeviceInfo__init(msg: *mut DeviceInfo) -> bool;
    fn industrial_msgs__msg__DeviceInfo__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<DeviceInfo>, size: usize) -> bool;
    fn industrial_msgs__msg__DeviceInfo__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<DeviceInfo>);
    fn industrial_msgs__msg__DeviceInfo__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<DeviceInfo>, out_seq: *mut rosidl_runtime_rs::Sequence<DeviceInfo>) -> bool;
}

// Corresponds to industrial_msgs__msg__DeviceInfo
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Device info captures device agnostic information about a piece of hardware.
/// This message is meant as a generic as possible.  Items that don't apply should
/// be left blank.  This message is not meant to replace diagnostic messages, but
/// rather provide a standard service message that can be used to populate standard
/// components (like a GUI for example)

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeviceInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub serial_number: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hw_version: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sw_version: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub address: rosidl_runtime_rs::String,

}



impl Default for DeviceInfo {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !industrial_msgs__msg__DeviceInfo__init(&mut msg as *mut _) {
        panic!("Call to industrial_msgs__msg__DeviceInfo__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for DeviceInfo {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__DeviceInfo__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__DeviceInfo__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__DeviceInfo__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for DeviceInfo {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for DeviceInfo where Self: Sized {
  const TYPE_NAME: &'static str = "industrial_msgs/msg/DeviceInfo";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__DeviceInfo() }
  }
}


#[link(name = "industrial_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__RobotMode() -> *const std::ffi::c_void;
}

#[link(name = "industrial_msgs__rosidl_generator_c")]
extern "C" {
    fn industrial_msgs__msg__RobotMode__init(msg: *mut RobotMode) -> bool;
    fn industrial_msgs__msg__RobotMode__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotMode>, size: usize) -> bool;
    fn industrial_msgs__msg__RobotMode__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotMode>);
    fn industrial_msgs__msg__RobotMode__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotMode>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotMode>) -> bool;
}

// Corresponds to industrial_msgs__msg__RobotMode
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// The Robot mode message encapsulates the mode/teach state of the robot
/// Typically this is controlled by the pendant key switch, but not always

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotMode {

    // This member is not documented.
    #[allow(missing_docs)]
    pub val: i8,

}

impl RobotMode {
    /// enumerated values
    /// Unknown or unavailable
    pub const UNKNOWN: i8 = -1;

    /// Teach OR manual mode
    pub const MANUAL: i8 = 1;

    /// Automatic mode
    pub const AUTO: i8 = 2;

}


impl Default for RobotMode {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !industrial_msgs__msg__RobotMode__init(&mut msg as *mut _) {
        panic!("Call to industrial_msgs__msg__RobotMode__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotMode {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__RobotMode__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__RobotMode__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__RobotMode__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotMode {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotMode where Self: Sized {
  const TYPE_NAME: &'static str = "industrial_msgs/msg/RobotMode";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__RobotMode() }
  }
}


#[link(name = "industrial_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__RobotStatus() -> *const std::ffi::c_void;
}

#[link(name = "industrial_msgs__rosidl_generator_c")]
extern "C" {
    fn industrial_msgs__msg__RobotStatus__init(msg: *mut RobotStatus) -> bool;
    fn industrial_msgs__msg__RobotStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<RobotStatus>, size: usize) -> bool;
    fn industrial_msgs__msg__RobotStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<RobotStatus>);
    fn industrial_msgs__msg__RobotStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<RobotStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<RobotStatus>) -> bool;
}

// Corresponds to industrial_msgs__msg__RobotStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// The RobotStatus message contains low level status information 
/// that is specific to an industrial robot controller

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotStatus {
    /// The header frame ID is not used
    pub header: std_msgs::msg::rmw::Header,

    /// The robot mode captures the operating mode of the robot.  When in
    /// manual, remote motion is not possible.
    pub mode: super::super::msg::rmw::RobotMode,

    /// Estop status: True if robot is e-stopped.  The drives are disabled
    /// and motion is not possible.  The e-stop condition must be acknowledged
    /// and cleared before any motion can begin.
    pub e_stopped: super::super::msg::rmw::TriState,

    /// Drive power status: True if drives are powered.  Motion commands will
    /// automatically enable the drives if required.  Drive power is not requred
    /// for possible motion
    pub drives_powered: super::super::msg::rmw::TriState,

    /// Motion enabled: True if robot motion is possible.
    pub motion_possible: super::super::msg::rmw::TriState,

    /// Motion status: True if robot is in motion, otherwise false
    pub in_motion: super::super::msg::rmw::TriState,

    /// Error status: True if there is an error condition on the robot. Motion may
    /// or may not be affected (see motion_possible)
    pub in_error: super::super::msg::rmw::TriState,

    /// Error code: Vendor specific error codes. If this list is empty, there are
    /// no active errors on the controller. Order of entries in this list does
    /// not necessarily encode for any specific severity or priority of active
    /// errors.
    pub error_codes: rosidl_runtime_rs::Sequence<i32>,

}



impl Default for RobotStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !industrial_msgs__msg__RobotStatus__init(&mut msg as *mut _) {
        panic!("Call to industrial_msgs__msg__RobotStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for RobotStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__RobotStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__RobotStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__RobotStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for RobotStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for RobotStatus where Self: Sized {
  const TYPE_NAME: &'static str = "industrial_msgs/msg/RobotStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__RobotStatus() }
  }
}


#[link(name = "industrial_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__ServiceReturnCode() -> *const std::ffi::c_void;
}

#[link(name = "industrial_msgs__rosidl_generator_c")]
extern "C" {
    fn industrial_msgs__msg__ServiceReturnCode__init(msg: *mut ServiceReturnCode) -> bool;
    fn industrial_msgs__msg__ServiceReturnCode__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ServiceReturnCode>, size: usize) -> bool;
    fn industrial_msgs__msg__ServiceReturnCode__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ServiceReturnCode>);
    fn industrial_msgs__msg__ServiceReturnCode__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ServiceReturnCode>, out_seq: *mut rosidl_runtime_rs::Sequence<ServiceReturnCode>) -> bool;
}

// Corresponds to industrial_msgs__msg__ServiceReturnCode
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Service return codes for simple requests.  All ROS-Industrial service
/// replies are required to have a return code indicating success or failure
/// Specific return codes for different failure should be negative.

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ServiceReturnCode {

    // This member is not documented.
    #[allow(missing_docs)]
    pub val: i8,

}

impl ServiceReturnCode {

    // This constant is not documented.
    #[allow(missing_docs)]
    pub const SUCCESS: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const FAILURE: i8 = -1;

}


impl Default for ServiceReturnCode {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !industrial_msgs__msg__ServiceReturnCode__init(&mut msg as *mut _) {
        panic!("Call to industrial_msgs__msg__ServiceReturnCode__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ServiceReturnCode {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__ServiceReturnCode__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__ServiceReturnCode__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__ServiceReturnCode__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ServiceReturnCode {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ServiceReturnCode where Self: Sized {
  const TYPE_NAME: &'static str = "industrial_msgs/msg/ServiceReturnCode";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__ServiceReturnCode() }
  }
}


#[link(name = "industrial_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__TriState() -> *const std::ffi::c_void;
}

#[link(name = "industrial_msgs__rosidl_generator_c")]
extern "C" {
    fn industrial_msgs__msg__TriState__init(msg: *mut TriState) -> bool;
    fn industrial_msgs__msg__TriState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<TriState>, size: usize) -> bool;
    fn industrial_msgs__msg__TriState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<TriState>);
    fn industrial_msgs__msg__TriState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<TriState>, out_seq: *mut rosidl_runtime_rs::Sequence<TriState>) -> bool;
}

// Corresponds to industrial_msgs__msg__TriState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// The tri-state captures boolean values with the additional state of unknown

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct TriState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub val: i8,

}

impl TriState {
    /// enumerated values
    /// Unknown or unavailable
    pub const UNKNOWN: i8 = -1;

    /// High state
    pub const TRUE: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ON: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const ENABLED: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const HIGH: i8 = 1;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const CLOSED: i8 = 1;

    /// Low state
    pub const FALSE: i8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const OFF: i8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const DISABLED: i8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const LOW: i8 = 0;


    // This constant is not documented.
    #[allow(missing_docs)]
    pub const OPEN: i8 = 0;

}


impl Default for TriState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !industrial_msgs__msg__TriState__init(&mut msg as *mut _) {
        panic!("Call to industrial_msgs__msg__TriState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for TriState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__TriState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__TriState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { industrial_msgs__msg__TriState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for TriState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for TriState where Self: Sized {
  const TYPE_NAME: &'static str = "industrial_msgs/msg/TriState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__industrial_msgs__msg__TriState() }
  }
}


