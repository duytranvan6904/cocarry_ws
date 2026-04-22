#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



#[link(name = "human_hand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__srv__SelectModel_Request() -> *const std::ffi::c_void;
}

#[link(name = "human_hand_msgs__rosidl_generator_c")]
extern "C" {
    fn human_hand_msgs__srv__SelectModel_Request__init(msg: *mut SelectModel_Request) -> bool;
    fn human_hand_msgs__srv__SelectModel_Request__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SelectModel_Request>, size: usize) -> bool;
    fn human_hand_msgs__srv__SelectModel_Request__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SelectModel_Request>);
    fn human_hand_msgs__srv__SelectModel_Request__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SelectModel_Request>, out_seq: *mut rosidl_runtime_rs::Sequence<SelectModel_Request>) -> bool;
}

// Corresponds to human_hand_msgs__srv__SelectModel_Request
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectModel_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model_name: rosidl_runtime_rs::String,

}



impl Default for SelectModel_Request {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !human_hand_msgs__srv__SelectModel_Request__init(&mut msg as *mut _) {
        panic!("Call to human_hand_msgs__srv__SelectModel_Request__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SelectModel_Request {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__srv__SelectModel_Request__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__srv__SelectModel_Request__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__srv__SelectModel_Request__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SelectModel_Request {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SelectModel_Request where Self: Sized {
  const TYPE_NAME: &'static str = "human_hand_msgs/srv/SelectModel_Request";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__srv__SelectModel_Request() }
  }
}


#[link(name = "human_hand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__srv__SelectModel_Response() -> *const std::ffi::c_void;
}

#[link(name = "human_hand_msgs__rosidl_generator_c")]
extern "C" {
    fn human_hand_msgs__srv__SelectModel_Response__init(msg: *mut SelectModel_Response) -> bool;
    fn human_hand_msgs__srv__SelectModel_Response__Sequence__init(seq: *mut rosidl_runtime_rs::Sequence<SelectModel_Response>, size: usize) -> bool;
    fn human_hand_msgs__srv__SelectModel_Response__Sequence__fini(seq: *mut rosidl_runtime_rs::Sequence<SelectModel_Response>);
    fn human_hand_msgs__srv__SelectModel_Response__Sequence__copy(in_seq: &rosidl_runtime_rs::Sequence<SelectModel_Response>, out_seq: *mut rosidl_runtime_rs::Sequence<SelectModel_Response>) -> bool;
}

// Corresponds to human_hand_msgs__srv__SelectModel_Response
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]


// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[repr(C)]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectModel_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: rosidl_runtime_rs::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub active_model: rosidl_runtime_rs::String,

}



impl Default for SelectModel_Response {
  fn default() -> Self {
    unsafe {
      let mut msg = std::mem::zeroed();
      if !human_hand_msgs__srv__SelectModel_Response__init(&mut msg as *mut _) {
        panic!("Call to human_hand_msgs__srv__SelectModel_Response__init() failed");
      }
      msg
    }
  }
}

impl rosidl_runtime_rs::SequenceAlloc for SelectModel_Response {
  fn sequence_init(seq: &mut rosidl_runtime_rs::Sequence<Self>, size: usize) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__srv__SelectModel_Response__Sequence__init(seq as *mut _, size) }
  }
  fn sequence_fini(seq: &mut rosidl_runtime_rs::Sequence<Self>) {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__srv__SelectModel_Response__Sequence__fini(seq as *mut _) }
  }
  fn sequence_copy(in_seq: &rosidl_runtime_rs::Sequence<Self>, out_seq: &mut rosidl_runtime_rs::Sequence<Self>) -> bool {
    // SAFETY: This is safe since the pointer is guaranteed to be valid/initialized.
    unsafe { human_hand_msgs__srv__SelectModel_Response__Sequence__copy(in_seq, out_seq as *mut _) }
  }
}

impl rosidl_runtime_rs::Message for SelectModel_Response {
  type RmwMsg = Self;
  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> { msg_cow }
  fn from_rmw_message(msg: Self::RmwMsg) -> Self { msg }
}

impl rosidl_runtime_rs::RmwMessage for SelectModel_Response where Self: Sized {
  const TYPE_NAME: &'static str = "human_hand_msgs/srv/SelectModel_Response";
  fn get_type_support() -> *const std::ffi::c_void {
    // SAFETY: No preconditions for this function.
    unsafe { rosidl_typesupport_c__get_message_type_support_handle__human_hand_msgs__srv__SelectModel_Response() }
  }
}






#[link(name = "human_hand_msgs__rosidl_typesupport_c")]
extern "C" {
    fn rosidl_typesupport_c__get_service_type_support_handle__human_hand_msgs__srv__SelectModel() -> *const std::ffi::c_void;
}

// Corresponds to human_hand_msgs__srv__SelectModel
#[allow(missing_docs, non_camel_case_types)]
pub struct SelectModel;

impl rosidl_runtime_rs::Service for SelectModel {
    type Request = SelectModel_Request;
    type Response = SelectModel_Response;

    fn get_type_support() -> *const std::ffi::c_void {
        // SAFETY: No preconditions for this function.
        unsafe { rosidl_typesupport_c__get_service_type_support_handle__human_hand_msgs__srv__SelectModel() }
    }
}


