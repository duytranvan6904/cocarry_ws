#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};


#[link(name = "human_hand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__msg__HandState() -> *const std::ffi::c_void;
}

#[link(name = "human_hand_msgs__rosidl_generator_c")]
extern "C" {
    fn human_hand_msgs__msg__HandState__init(msg: *mut HandState) -> bool;
    fn human_hand_msgs__msg__HandState__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<HandState>, size: usize) -> bool;
    fn human_hand_msgs__msg__HandState__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<HandState>);
    fn human_hand_msgs__msg__HandState__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<HandState>, out_seq: *mut rosidl_runtime_rs::Sequence<HandState>) -> bool;
}

// Corresponds to human_hand_msgs__msg__HandState
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Measured hand position from camera (world frame, post-calibration)

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct HandState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub tracking_id: u64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub is_tracked: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub confidence: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub source: rosidl_runtime_rs::String,

}



impl Default for HandState {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !human_hand_msgs__msg__HandState__init(&mut msg as *mut _) {
        panic!("Call to human_hand_msgs__msg__HandState__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for HandState {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__HandState__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__HandState__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__HandState__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for HandState {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for HandState where Self: Sized {
  const TYPE_NAME: &'static str = "human_hand_msgs/msg/HandState";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__msg__HandState() }
  }
}


#[link(name = "human_hand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__msg__HandPrediction() -> *const std::ffi::c_void;
}

#[link(name = "human_hand_msgs__rosidl_generator_c")]
extern "C" {
    fn human_hand_msgs__msg__HandPrediction__init(msg: *mut HandPrediction) -> bool;
    fn human_hand_msgs__msg__HandPrediction__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<HandPrediction>, size: usize) -> bool;
    fn human_hand_msgs__msg__HandPrediction__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<HandPrediction>);
    fn human_hand_msgs__msg__HandPrediction__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<HandPrediction>, out_seq: *mut rosidl_runtime_rs::Sequence<HandPrediction>) -> bool;
}

// Corresponds to human_hand_msgs__msg__HandPrediction
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// Predicted next hand position from ML model

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct HandPrediction {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub x: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub y: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub z: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub inference_time_ms: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub model_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub buffer_size: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub prediction_confidence: f64,

}



impl Default for HandPrediction {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !human_hand_msgs__msg__HandPrediction__init(&mut msg as *mut _) {
        panic!("Call to human_hand_msgs__msg__HandPrediction__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for HandPrediction {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__HandPrediction__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__HandPrediction__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__HandPrediction__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for HandPrediction {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for HandPrediction where Self: Sized {
  const TYPE_NAME: &'static str = "human_hand_msgs/msg/HandPrediction";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__msg__HandPrediction() }
  }
}


#[link(name = "human_hand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__msg__SystemStatus() -> *const std::ffi::c_void;
}

#[link(name = "human_hand_msgs__rosidl_generator_c")]
extern "C" {
    fn human_hand_msgs__msg__SystemStatus__init(msg: *mut SystemStatus) -> bool;
    fn human_hand_msgs__msg__SystemStatus__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SystemStatus>, size: usize) -> bool;
    fn human_hand_msgs__msg__SystemStatus__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SystemStatus>);
    fn human_hand_msgs__msg__SystemStatus__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SystemStatus>, out_seq: *mut rosidl_runtime_rs::Sequence<SystemStatus>) -> bool;
}

// Corresponds to human_hand_msgs__msg__SystemStatus
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]

/// System monitoring status

#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SystemStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::rmw::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub node_name: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fps: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub latency_ms: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,

}



impl Default for SystemStatus {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !human_hand_msgs__msg__SystemStatus__init(&mut msg as *mut _) {
        panic!("Call to human_hand_msgs__msg__SystemStatus__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SystemStatus {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__SystemStatus__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__SystemStatus__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__msg__SystemStatus__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SystemStatus {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SystemStatus where Self: Sized {
  const TYPE_NAME: &'static str = "human_hand_msgs/msg/SystemStatus";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__msg__SystemStatus() }
  }
}


