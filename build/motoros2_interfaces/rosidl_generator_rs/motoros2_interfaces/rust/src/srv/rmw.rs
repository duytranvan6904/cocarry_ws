#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__GetActiveAlarmInfo_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Request__init(msg: *mut GetActiveAlarmInfo_Request) -> bool;
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Request>);
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__GetActiveAlarmInfo_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetActiveAlarmInfo_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetActiveAlarmInfo_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__GetActiveAlarmInfo_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__GetActiveAlarmInfo_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetActiveAlarmInfo_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__GetActiveAlarmInfo_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__GetActiveAlarmInfo_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__GetActiveAlarmInfo_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetActiveAlarmInfo_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetActiveAlarmInfo_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/GetActiveAlarmInfo_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__GetActiveAlarmInfo_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__GetActiveAlarmInfo_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Response__init(msg: *mut GetActiveAlarmInfo_Response) -> bool;
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Response>);
    fn motoros2_interfaces__srv__GetActiveAlarmInfo_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<GetActiveAlarmInfo_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__GetActiveAlarmInfo_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetActiveAlarmInfo_Response {
    /// Result of the service invocation. Values other than one (1) signal failure.
    ///
    /// NOTE: future versions of this service may use a different set of result codes
    pub result_code: u32,

    /// string representation of the value in 'result_code', for humans
    pub result_message: rosidl_runtime_rs::String,

    /// Each entry in this list provides detailed information about all currently
    /// active alarms. If this list is empty, there are no active alarms.
    ///
    /// Note: order of entries in this list does not encode for any specific severity
    /// or priority of active alarms.
    pub alarms: rosidl_runtime_rs::Sequence<super::super::msg::rmw::AlarmInfo>,

    /// Each entry in this list provides detailed information about all currently
    /// active errors. If this list is empty, there are no active errors.
    ///
    /// Note: order of entries in this list does not encode for any specific severity
    /// or priority of active errors.
    pub errors: rosidl_runtime_rs::Sequence<super::super::msg::rmw::ErrorInfo>,

}



impl Default for GetActiveAlarmInfo_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__GetActiveAlarmInfo_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__GetActiveAlarmInfo_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for GetActiveAlarmInfo_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__GetActiveAlarmInfo_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__GetActiveAlarmInfo_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__GetActiveAlarmInfo_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for GetActiveAlarmInfo_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for GetActiveAlarmInfo_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/GetActiveAlarmInfo_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__GetActiveAlarmInfo_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ListInformJobs_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ListInformJobs_Request__init(msg: *mut ListInformJobs_Request) -> bool;
    fn motoros2_interfaces__srv__ListInformJobs_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ListInformJobs_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ListInformJobs_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ListInformJobs_Request>);
    fn motoros2_interfaces__srv__ListInformJobs_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ListInformJobs_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ListInformJobs_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ListInformJobs_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ListInformJobs_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ListInformJobs_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ListInformJobs_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ListInformJobs_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ListInformJobs_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ListInformJobs_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ListInformJobs_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ListInformJobs_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ListInformJobs_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ListInformJobs_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ListInformJobs_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ListInformJobs_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ListInformJobs_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ListInformJobs_Response__init(msg: *mut ListInformJobs_Response) -> bool;
    fn motoros2_interfaces__srv__ListInformJobs_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ListInformJobs_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ListInformJobs_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ListInformJobs_Response>);
    fn motoros2_interfaces__srv__ListInformJobs_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ListInformJobs_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ListInformJobs_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ListInformJobs_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ListInformJobs_Response {
    /// Result of the service invocation. Values other than one (1) signal failure.
    ///
    /// Values defined in 'motoros2_interfaces/msg/InformJobCrudResultCodes'.
    ///
    /// NOTE: future versions of this service may use a different set of result
    /// codes. Always make sure to compare against defined named constants instead
    /// of integers directly.
    pub result_code: u32,

    /// string representation of the value in 'result_code', for humans
    pub message: rosidl_runtime_rs::String,

    /// The list of jobs present on the controller.
    ///
    /// NOTE:
    /// - these are job names, not filenames, and thus will not include the file
    ///   extension (JBI)
    /// - character encodings other than ASCII are only partially supported
    pub names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,

}



impl Default for ListInformJobs_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ListInformJobs_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ListInformJobs_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ListInformJobs_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ListInformJobs_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ListInformJobs_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ListInformJobs_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ListInformJobs_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ListInformJobs_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ListInformJobs_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ListInformJobs_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__QueueTrajPoint_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__QueueTrajPoint_Request__init(msg: *mut QueueTrajPoint_Request) -> bool;
    fn motoros2_interfaces__srv__QueueTrajPoint_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<QueueTrajPoint_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__QueueTrajPoint_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<QueueTrajPoint_Request>);
    fn motoros2_interfaces__srv__QueueTrajPoint_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<QueueTrajPoint_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<QueueTrajPoint_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__QueueTrajPoint_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QueueTrajPoint_Request {
    /// Submit a trajectory point to the continuous motion queue.
    ///
    /// The start_point_queue_mode service must have been invoked first
    pub joint_names: rosidl_runtime_rs::Sequence<rosidl_runtime_rs::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub point: trajectory_msgs::msg::rmw::JointTrajectoryPoint,

}



impl Default for QueueTrajPoint_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__QueueTrajPoint_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__QueueTrajPoint_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for QueueTrajPoint_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__QueueTrajPoint_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__QueueTrajPoint_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__QueueTrajPoint_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for QueueTrajPoint_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for QueueTrajPoint_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/QueueTrajPoint_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__QueueTrajPoint_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__QueueTrajPoint_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__QueueTrajPoint_Response__init(msg: *mut QueueTrajPoint_Response) -> bool;
    fn motoros2_interfaces__srv__QueueTrajPoint_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<QueueTrajPoint_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__QueueTrajPoint_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<QueueTrajPoint_Response>);
    fn motoros2_interfaces__srv__QueueTrajPoint_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<QueueTrajPoint_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<QueueTrajPoint_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__QueueTrajPoint_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QueueTrajPoint_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::super::msg::rmw::QueueResultEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: rosidl_runtime_rs::String,

}



impl Default for QueueTrajPoint_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__QueueTrajPoint_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__QueueTrajPoint_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for QueueTrajPoint_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__QueueTrajPoint_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__QueueTrajPoint_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__QueueTrajPoint_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for QueueTrajPoint_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for QueueTrajPoint_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/QueueTrajPoint_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__QueueTrajPoint_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadMRegister_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ReadMRegister_Request__init(msg: *mut ReadMRegister_Request) -> bool;
    fn motoros2_interfaces__srv__ReadMRegister_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadMRegister_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ReadMRegister_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadMRegister_Request>);
    fn motoros2_interfaces__srv__ReadMRegister_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadMRegister_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadMRegister_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ReadMRegister_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadMRegister_Request {
    /// Read (and return) the current value of the M register at 'address'.
    ///
    /// Addresses are plain, base-10 integers, as used and displayed by the controller
    /// (on the teach pendant for instance).
    ///
    /// Only the following addresses can be read from:
    ///
    ///  - 0 to 999
    ///
    /// NOTE 1: do not add 1000000 to the address, MotoROS will do this when
    ///         necessary.
    ///
    /// NOTE 2: many programming languages will parse literals starting with '0' as
    ///         octal numbers. Do not add leading zeros to register addresses to avoid
    ///         specifying the wrong register to read.
    ///
    /// Refer also the Yaskawa Motoman documentation on IO addressing and
    /// configuration.
    pub address: u32,

}



impl Default for ReadMRegister_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ReadMRegister_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ReadMRegister_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadMRegister_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadMRegister_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadMRegister_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadMRegister_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadMRegister_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadMRegister_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ReadMRegister_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadMRegister_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadMRegister_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ReadMRegister_Response__init(msg: *mut ReadMRegister_Response) -> bool;
    fn motoros2_interfaces__srv__ReadMRegister_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadMRegister_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ReadMRegister_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadMRegister_Response>);
    fn motoros2_interfaces__srv__ReadMRegister_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadMRegister_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadMRegister_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ReadMRegister_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadMRegister_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u16,

}



impl Default for ReadMRegister_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ReadMRegister_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ReadMRegister_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadMRegister_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadMRegister_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadMRegister_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadMRegister_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadMRegister_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadMRegister_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ReadMRegister_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadMRegister_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadSingleIO_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ReadSingleIO_Request__init(msg: *mut ReadSingleIO_Request) -> bool;
    fn motoros2_interfaces__srv__ReadSingleIO_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadSingleIO_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ReadSingleIO_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadSingleIO_Request>);
    fn motoros2_interfaces__srv__ReadSingleIO_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadSingleIO_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadSingleIO_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ReadSingleIO_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadSingleIO_Request {
    /// Read (and return) the current value of the IO element at 'address'.
    ///
    /// Addresses are plain, base-10 integers, as used and displayed by the controller
    /// (on the teach pendant for instance).
    ///
    /// There are no restrictions as to which IO elements can be read, but they have
    /// to exist on the controller and be configured correctly.
    ///
    /// Refer also the Yaskawa Motoman documentation on IO addressing and
    /// configuration.
    pub address: u32,

}



impl Default for ReadSingleIO_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ReadSingleIO_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ReadSingleIO_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadSingleIO_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadSingleIO_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadSingleIO_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadSingleIO_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadSingleIO_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadSingleIO_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ReadSingleIO_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadSingleIO_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadSingleIO_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ReadSingleIO_Response__init(msg: *mut ReadSingleIO_Response) -> bool;
    fn motoros2_interfaces__srv__ReadSingleIO_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadSingleIO_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ReadSingleIO_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadSingleIO_Response>);
    fn motoros2_interfaces__srv__ReadSingleIO_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadSingleIO_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadSingleIO_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ReadSingleIO_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadSingleIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for ReadSingleIO_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ReadSingleIO_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ReadSingleIO_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadSingleIO_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadSingleIO_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadSingleIO_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadSingleIO_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadSingleIO_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadSingleIO_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ReadSingleIO_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadSingleIO_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadGroupIO_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ReadGroupIO_Request__init(msg: *mut ReadGroupIO_Request) -> bool;
    fn motoros2_interfaces__srv__ReadGroupIO_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadGroupIO_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ReadGroupIO_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadGroupIO_Request>);
    fn motoros2_interfaces__srv__ReadGroupIO_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadGroupIO_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadGroupIO_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ReadGroupIO_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadGroupIO_Request {
    /// Read (and return) the current value of the Group IO element at 'address'.
    ///
    /// Addresses are plain, base-10 integers, as used and displayed by the controller
    /// (on the teach pendant for instance).
    ///
    /// There are no restrictions as to which group IO elements can be read, but they
    /// have to exist on the controller and be configured correctly.
    ///
    /// NOTE: many programming languages will parse literals starting with '0' as
    ///       octal numbers. Do not add leading zeros to group addresses to avoid
    ///       specifying the wrong address to read.
    ///
    /// Refer also the Yaskawa Motoman documentation on IO addressing and
    /// configuration.
    pub address: u32,

}



impl Default for ReadGroupIO_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ReadGroupIO_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ReadGroupIO_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadGroupIO_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadGroupIO_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadGroupIO_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadGroupIO_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadGroupIO_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadGroupIO_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ReadGroupIO_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadGroupIO_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadGroupIO_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ReadGroupIO_Response__init(msg: *mut ReadGroupIO_Response) -> bool;
    fn motoros2_interfaces__srv__ReadGroupIO_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ReadGroupIO_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ReadGroupIO_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ReadGroupIO_Response>);
    fn motoros2_interfaces__srv__ReadGroupIO_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ReadGroupIO_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ReadGroupIO_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ReadGroupIO_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadGroupIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u8,

}



impl Default for ReadGroupIO_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ReadGroupIO_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ReadGroupIO_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ReadGroupIO_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadGroupIO_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadGroupIO_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ReadGroupIO_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ReadGroupIO_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ReadGroupIO_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ReadGroupIO_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ReadGroupIO_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ResetError_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ResetError_Request__init(msg: *mut ResetError_Request) -> bool;
    fn motoros2_interfaces__srv__ResetError_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ResetError_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ResetError_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ResetError_Request>);
    fn motoros2_interfaces__srv__ResetError_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ResetError_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<ResetError_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ResetError_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ResetError_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ResetError_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ResetError_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ResetError_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ResetError_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ResetError_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ResetError_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ResetError_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ResetError_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ResetError_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ResetError_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ResetError_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ResetError_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__ResetError_Response__init(msg: *mut ResetError_Response) -> bool;
    fn motoros2_interfaces__srv__ResetError_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<ResetError_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__ResetError_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<ResetError_Response>);
    fn motoros2_interfaces__srv__ResetError_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<ResetError_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<ResetError_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__ResetError_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ResetError_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::super::msg::rmw::MotionReadyEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: rosidl_runtime_rs::String,

}



impl Default for ResetError_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__ResetError_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__ResetError_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for ResetError_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ResetError_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ResetError_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__ResetError_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for ResetError_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for ResetError_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/ResetError_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__ResetError_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__SelectMotionTool_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__SelectMotionTool_Request__init(msg: *mut SelectMotionTool_Request) -> bool;
    fn motoros2_interfaces__srv__SelectMotionTool_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SelectMotionTool_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__SelectMotionTool_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SelectMotionTool_Request>);
    fn motoros2_interfaces__srv__SelectMotionTool_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SelectMotionTool_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SelectMotionTool_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__SelectMotionTool_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectMotionTool_Request {
    /// Change the active tool file used for motion on the controller.
    ///
    /// This changes the tool definition used for (Moto)ROS-controlled motions, not
    /// manual jogging.
    ///
    /// Make sure to read the following sections carefully to be aware
    /// of the behaviour of this service and of the Yaskawa controller after calling
    /// this service.
    ///
    /// ## FSU and PFL
    ///
    /// Tool switches through this service will be taken into account by the FSU and
    /// PFL safety systems if the controller has these options and they are enabled.
    ///
    /// Tool interference files, if associated with certain tool file definitions,
    /// will therefore also switch.
    ///
    /// ## Tool switch timing
    ///
    /// The active tool will be switched AFTER the controller has completed execution
    /// of the last trajectory segment that was sent to MotoROS BEFORE this service
    /// was called.
    ///
    /// The motion queue internal to MotoROS caches a number of segments in a FIFO.
    /// Only segments received AFTER this service was invoked will be executed with
    /// the new tool. Any segments received before a tool switch was invoked will use
    /// the old tool.
    ///
    /// To ensure motion will be executed using a certain tool, applications should
    /// check the 'in_motion' field (part of the RobotStatus message published on the
    /// 'robot_status' topic by the driver) and invoke the service when the robot has
    /// come to a stop (and the motion queue of MotoROS is empty). Any subsequent
    /// trajectories will use the new tool.
    ///
    /// ## Effect on trajectory execution
    ///
    /// As MotoROS currently only executes joint space trajectories, changing tool
    /// file with this service DOES NOT affect the execution of those trajectories.
    ///
    /// As noted earlier though, the active tool file definition will affect FSU and
    /// PFL behaviour, as the tool definition is used in calculation of dynamics and
    /// safety (see "FSU and PFL" above).
    ///
    /// To clarify: the TCP definition of the tool file is NOT taken into account when
    /// calculating manipulator motion based on incoming ROS JointTrajectoryAction
    /// goals (as JointTrajectory goals do not include any Cartesian poses, only
    /// absolute joint space coordinates for each axis).
    ///
    /// Instead, ROS applications should use different TF frames to define tool frames
    /// on the ROS side and plan their motions with the appropriate TF frame as the
    /// active tool.
    ///
    /// This service could then be used to notify the controller of other tool
    /// characteristics, such as weight, CoG and inertia by switching to a tool file
    /// configured with those parameters.
    ///
    /// ## Retrieving the active tool file
    ///
    /// MotoROS2 does not currently support retrieving the active tool file.
    ///
    /// For more information about tool file configuration, selection and use on
    /// Yaskawa controllers, refer to the relevant Yaskawa Motoman documentation.
    /// Numeric ID of the group the tool file is defined for.
    ///
    /// This MUST correspond to a group ID currently defined and active on the
    /// controller. The ROS service does not check whether the value specified here
    /// is legal. The MotoROS2 server will however check this, and will refuse to
    /// switch to an illegal value and will report this to the ROS driver.
    ///
    /// Callers will be notified of such failures by 'success' being set to 'false'
    /// and an appropriate error message being provided via the 'message' field of
    /// the service response.
    ///
    /// NOTE: this field is 0-based, with 0 corresponding to the first motion group,
    ///       1 the second, etc.
    ///
    /// legal-values: [0, total_nr_of_groups)
    /// required: yes (absence-causes-service-failure)
    /// default: no-default
    pub group_number: u32,

    /// Numeric ID of the tool file to switch to for the specified group.
    ///
    /// Identical to 'group_number', specification of illegal values will result
    /// in failure to invoke the MotoROS2 service, and an unsuccessful service result
    /// being returned.
    ///
    /// NOTE: this field is 0-based, with 0 corresponding to the first tool file,
    ///       1 the second, etc.
    ///
    /// legal-values: [0, 63]
    /// required: yes (absence-causes-service-failure)
    /// default: no-default
    pub tool_number: u32,

}



impl Default for SelectMotionTool_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__SelectMotionTool_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__SelectMotionTool_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SelectMotionTool_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__SelectMotionTool_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__SelectMotionTool_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__SelectMotionTool_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SelectMotionTool_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SelectMotionTool_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/SelectMotionTool_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__SelectMotionTool_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__SelectMotionTool_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__SelectMotionTool_Response__init(msg: *mut SelectMotionTool_Response) -> bool;
    fn motoros2_interfaces__srv__SelectMotionTool_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SelectMotionTool_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__SelectMotionTool_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SelectMotionTool_Response>);
    fn motoros2_interfaces__srv__SelectMotionTool_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SelectMotionTool_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SelectMotionTool_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__SelectMotionTool_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectMotionTool_Response {
    /// Result of the service invocation. Values other than zero (0) signal failure.
    ///
    /// Refer to SelectionResultCodes.msg for defined values
    pub result_code: super::super::msg::rmw::SelectionResultCodes,

    /// A human-readable error message, or an empty string if there was no error.
    pub message: rosidl_runtime_rs::String,

    /// true IFF invocation of the MotoROS service was successful.
    ///
    /// NOTE: this is independent of whether the ROS service invocation was
    ///       successful. In absence of any ROS middleware failures, a failed MotoROS
    ///       service invocation will result in 'success' here being set to 'false',
    ///       but a successful ROS service invocation.
    pub success: bool,

}



impl Default for SelectMotionTool_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__SelectMotionTool_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__SelectMotionTool_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SelectMotionTool_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__SelectMotionTool_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__SelectMotionTool_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__SelectMotionTool_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SelectMotionTool_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SelectMotionTool_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/SelectMotionTool_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__SelectMotionTool_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartTrajMode_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__StartTrajMode_Request__init(msg: *mut StartTrajMode_Request) -> bool;
    fn motoros2_interfaces__srv__StartTrajMode_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<StartTrajMode_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__StartTrajMode_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<StartTrajMode_Request>);
    fn motoros2_interfaces__srv__StartTrajMode_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<StartTrajMode_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<StartTrajMode_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__StartTrajMode_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartTrajMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for StartTrajMode_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__StartTrajMode_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__StartTrajMode_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for StartTrajMode_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartTrajMode_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartTrajMode_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartTrajMode_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for StartTrajMode_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for StartTrajMode_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/StartTrajMode_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartTrajMode_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartTrajMode_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__StartTrajMode_Response__init(msg: *mut StartTrajMode_Response) -> bool;
    fn motoros2_interfaces__srv__StartTrajMode_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<StartTrajMode_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__StartTrajMode_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<StartTrajMode_Response>);
    fn motoros2_interfaces__srv__StartTrajMode_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<StartTrajMode_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<StartTrajMode_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__StartTrajMode_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartTrajMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::super::msg::rmw::MotionReadyEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: rosidl_runtime_rs::String,

}



impl Default for StartTrajMode_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__StartTrajMode_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__StartTrajMode_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for StartTrajMode_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartTrajMode_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartTrajMode_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartTrajMode_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for StartTrajMode_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for StartTrajMode_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/StartTrajMode_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartTrajMode_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartPointQueueMode_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__StartPointQueueMode_Request__init(msg: *mut StartPointQueueMode_Request) -> bool;
    fn motoros2_interfaces__srv__StartPointQueueMode_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<StartPointQueueMode_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__StartPointQueueMode_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<StartPointQueueMode_Request>);
    fn motoros2_interfaces__srv__StartPointQueueMode_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<StartPointQueueMode_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<StartPointQueueMode_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__StartPointQueueMode_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartPointQueueMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for StartPointQueueMode_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__StartPointQueueMode_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__StartPointQueueMode_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for StartPointQueueMode_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartPointQueueMode_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartPointQueueMode_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartPointQueueMode_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for StartPointQueueMode_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for StartPointQueueMode_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/StartPointQueueMode_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartPointQueueMode_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartPointQueueMode_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__StartPointQueueMode_Response__init(msg: *mut StartPointQueueMode_Response) -> bool;
    fn motoros2_interfaces__srv__StartPointQueueMode_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<StartPointQueueMode_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__StartPointQueueMode_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<StartPointQueueMode_Response>);
    fn motoros2_interfaces__srv__StartPointQueueMode_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<StartPointQueueMode_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<StartPointQueueMode_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__StartPointQueueMode_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartPointQueueMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::super::msg::rmw::MotionReadyEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: rosidl_runtime_rs::String,

}



impl Default for StartPointQueueMode_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__StartPointQueueMode_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__StartPointQueueMode_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for StartPointQueueMode_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartPointQueueMode_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartPointQueueMode_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__StartPointQueueMode_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for StartPointQueueMode_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for StartPointQueueMode_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/StartPointQueueMode_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__StartPointQueueMode_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteMRegister_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__WriteMRegister_Request__init(msg: *mut WriteMRegister_Request) -> bool;
    fn motoros2_interfaces__srv__WriteMRegister_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WriteMRegister_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__WriteMRegister_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WriteMRegister_Request>);
    fn motoros2_interfaces__srv__WriteMRegister_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WriteMRegister_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<WriteMRegister_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__WriteMRegister_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteMRegister_Request {
    /// Write 'value' to the M register at 'address'.
    ///
    /// Addresses are plain, base-10 integers, as used and displayed by the controller
    /// (on the teach pendant for instance).
    ///
    /// Only the following addresses can be written to:
    ///
    ///  - 0 to 559
    ///
    /// NOTE 1: do not add 1000000 to the address, MotoROS will do this when
    ///         necessary.
    ///
    /// NOTE 2: many programming languages will parse literals starting with '0' as
    ///         octal numbers. Do not add leading zeros to register addresses to avoid
    ///         specifying the wrong register to write to.
    ///
    /// Refer also the Yaskawa Motoman documentation on IO addressing and
    /// configuration.
    pub address: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u16,

}



impl Default for WriteMRegister_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__WriteMRegister_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__WriteMRegister_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WriteMRegister_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteMRegister_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteMRegister_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteMRegister_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WriteMRegister_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WriteMRegister_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/WriteMRegister_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteMRegister_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteMRegister_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__WriteMRegister_Response__init(msg: *mut WriteMRegister_Response) -> bool;
    fn motoros2_interfaces__srv__WriteMRegister_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WriteMRegister_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__WriteMRegister_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WriteMRegister_Response>);
    fn motoros2_interfaces__srv__WriteMRegister_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WriteMRegister_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<WriteMRegister_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__WriteMRegister_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteMRegister_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for WriteMRegister_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__WriteMRegister_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__WriteMRegister_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WriteMRegister_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteMRegister_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteMRegister_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteMRegister_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WriteMRegister_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WriteMRegister_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/WriteMRegister_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteMRegister_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteSingleIO_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__WriteSingleIO_Request__init(msg: *mut WriteSingleIO_Request) -> bool;
    fn motoros2_interfaces__srv__WriteSingleIO_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WriteSingleIO_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__WriteSingleIO_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WriteSingleIO_Request>);
    fn motoros2_interfaces__srv__WriteSingleIO_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WriteSingleIO_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<WriteSingleIO_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__WriteSingleIO_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteSingleIO_Request {
    /// Write 'value' to the IO element at 'address'.
    ///
    /// This service does not return anything.
    ///
    /// Addresses are plain, base-10 integers, as used and displayed by the controller
    /// (on the teach pendant for instance).
    ///
    /// Only the following addresses can be written to:
    ///
    ///  - 27010 and up : Network Inputs (25010 and up on DX100 and FS100)
    ///  - 10010 and up : Universal/General Outputs
    ///
    /// Refer also the Yaskawa Motoman documentation on IO addressing and
    /// configuration.
    pub address: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for WriteSingleIO_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__WriteSingleIO_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__WriteSingleIO_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WriteSingleIO_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteSingleIO_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteSingleIO_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteSingleIO_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WriteSingleIO_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WriteSingleIO_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/WriteSingleIO_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteSingleIO_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteSingleIO_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__WriteSingleIO_Response__init(msg: *mut WriteSingleIO_Response) -> bool;
    fn motoros2_interfaces__srv__WriteSingleIO_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WriteSingleIO_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__WriteSingleIO_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WriteSingleIO_Response>);
    fn motoros2_interfaces__srv__WriteSingleIO_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WriteSingleIO_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<WriteSingleIO_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__WriteSingleIO_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteSingleIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for WriteSingleIO_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__WriteSingleIO_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__WriteSingleIO_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WriteSingleIO_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteSingleIO_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteSingleIO_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteSingleIO_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WriteSingleIO_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WriteSingleIO_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/WriteSingleIO_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteSingleIO_Response() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteGroupIO_Request() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__WriteGroupIO_Request__init(msg: *mut WriteGroupIO_Request) -> bool;
    fn motoros2_interfaces__srv__WriteGroupIO_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WriteGroupIO_Request>, size: usize) -> bool;
    fn motoros2_interfaces__srv__WriteGroupIO_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WriteGroupIO_Request>);
    fn motoros2_interfaces__srv__WriteGroupIO_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WriteGroupIO_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<WriteGroupIO_Request>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__WriteGroupIO_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteGroupIO_Request {
    /// Write 'value' to the Group IO element at 'address'.
    ///
    /// Addresses are plain, base-10 integers, as used and displayed by the controller
    /// (on the teach pendant for instance).
    ///
    /// Only the following addresses can be written to:
    ///
    ///  - 2701 and up : Network Inputs (2501 and up on DX100 and FS100)
    ///  - 1001 and up : Universal/General Outputs
    ///
    /// NOTE: many programming languages will parse literals starting with '0' as
    ///       octal numbers. Do not add leading zeros to group addresses to avoid
    ///       specifying the wrong address to write to.
    /// Refer also the Yaskawa Motoman documentation on IO addressing and
    /// configuration.
    pub address: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u8,

}



impl Default for WriteGroupIO_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__WriteGroupIO_Request__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__WriteGroupIO_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WriteGroupIO_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteGroupIO_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteGroupIO_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteGroupIO_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WriteGroupIO_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WriteGroupIO_Request where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/WriteGroupIO_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteGroupIO_Request() }
  }
}


#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteGroupIO_Response() -> *const std::ffi::c_void;
}

#[link(name = "motoros2_interfaces__rosidl_generator_c")]
extern "C" {
    fn motoros2_interfaces__srv__WriteGroupIO_Response__init(msg: *mut WriteGroupIO_Response) -> bool;
    fn motoros2_interfaces__srv__WriteGroupIO_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<WriteGroupIO_Response>, size: usize) -> bool;
    fn motoros2_interfaces__srv__WriteGroupIO_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<WriteGroupIO_Response>);
    fn motoros2_interfaces__srv__WriteGroupIO_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<WriteGroupIO_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<WriteGroupIO_Response>) -> bool;
}

// Corresponds to motoros2_interfaces__srv__WriteGroupIO_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteGroupIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for WriteGroupIO_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !motoros2_interfaces__srv__WriteGroupIO_Response__init(&mut msg as *mut _) {
        panic!("Call to motoros2_interfaces__srv__WriteGroupIO_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for WriteGroupIO_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteGroupIO_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteGroupIO_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { motoros2_interfaces__srv__WriteGroupIO_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for WriteGroupIO_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for WriteGroupIO_Response where Self: Sized {
  const TYPE_NAME: &'static str = "motoros2_interfaces/srv/WriteGroupIO_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__motoros2_interfaces__srv__WriteGroupIO_Response() }
  }
}






#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__GetActiveAlarmInfo() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__GetActiveAlarmInfo
#[allow(missing_docs, non_camel_case_types)]
pub struct GetActiveAlarmInfo;

impl rosidl_runtime_rs::Service for GetActiveAlarmInfo {
    type Request = GetActiveAlarmInfo_Request;
    type Response = GetActiveAlarmInfo_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__GetActiveAlarmInfo() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ListInformJobs() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__ListInformJobs
#[allow(missing_docs, non_camel_case_types)]
pub struct ListInformJobs;

impl rosidl_runtime_rs::Service for ListInformJobs {
    type Request = ListInformJobs_Request;
    type Response = ListInformJobs_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ListInformJobs() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__QueueTrajPoint() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__QueueTrajPoint
#[allow(missing_docs, non_camel_case_types)]
pub struct QueueTrajPoint;

impl rosidl_runtime_rs::Service for QueueTrajPoint {
    type Request = QueueTrajPoint_Request;
    type Response = QueueTrajPoint_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__QueueTrajPoint() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ReadMRegister() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__ReadMRegister
#[allow(missing_docs, non_camel_case_types)]
pub struct ReadMRegister;

impl rosidl_runtime_rs::Service for ReadMRegister {
    type Request = ReadMRegister_Request;
    type Response = ReadMRegister_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ReadMRegister() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ReadSingleIO() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__ReadSingleIO
#[allow(missing_docs, non_camel_case_types)]
pub struct ReadSingleIO;

impl rosidl_runtime_rs::Service for ReadSingleIO {
    type Request = ReadSingleIO_Request;
    type Response = ReadSingleIO_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ReadSingleIO() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ReadGroupIO() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__ReadGroupIO
#[allow(missing_docs, non_camel_case_types)]
pub struct ReadGroupIO;

impl rosidl_runtime_rs::Service for ReadGroupIO {
    type Request = ReadGroupIO_Request;
    type Response = ReadGroupIO_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ReadGroupIO() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ResetError() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__ResetError
#[allow(missing_docs, non_camel_case_types)]
pub struct ResetError;

impl rosidl_runtime_rs::Service for ResetError {
    type Request = ResetError_Request;
    type Response = ResetError_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__ResetError() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__SelectMotionTool() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__SelectMotionTool
#[allow(missing_docs, non_camel_case_types)]
pub struct SelectMotionTool;

impl rosidl_runtime_rs::Service for SelectMotionTool {
    type Request = SelectMotionTool_Request;
    type Response = SelectMotionTool_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__SelectMotionTool() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__StartTrajMode() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__StartTrajMode
#[allow(missing_docs, non_camel_case_types)]
pub struct StartTrajMode;

impl rosidl_runtime_rs::Service for StartTrajMode {
    type Request = StartTrajMode_Request;
    type Response = StartTrajMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__StartTrajMode() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__StartPointQueueMode() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__StartPointQueueMode
#[allow(missing_docs, non_camel_case_types)]
pub struct StartPointQueueMode;

impl rosidl_runtime_rs::Service for StartPointQueueMode {
    type Request = StartPointQueueMode_Request;
    type Response = StartPointQueueMode_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__StartPointQueueMode() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__WriteMRegister() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__WriteMRegister
#[allow(missing_docs, non_camel_case_types)]
pub struct WriteMRegister;

impl rosidl_runtime_rs::Service for WriteMRegister {
    type Request = WriteMRegister_Request;
    type Response = WriteMRegister_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__WriteMRegister() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__WriteSingleIO() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__WriteSingleIO
#[allow(missing_docs, non_camel_case_types)]
pub struct WriteSingleIO;

impl rosidl_runtime_rs::Service for WriteSingleIO {
    type Request = WriteSingleIO_Request;
    type Response = WriteSingleIO_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__WriteSingleIO() }
    }
}




#[link(name = "motoros2_interfaces__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__WriteGroupIO() -> *const std::ffi::c_void;
}

// Corresponds to motoros2_interfaces__srv__WriteGroupIO
#[allow(missing_docs, non_camel_case_types)]
pub struct WriteGroupIO;

impl rosidl_runtime_rs::Service for WriteGroupIO {
    type Request = WriteGroupIO_Request;
    type Response = WriteGroupIO_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__motoros2_interfaces__srv__WriteGroupIO() }
    }
}


