#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to human_hand_msgs__srv__SelectModel_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectModel_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model_name: std::string::String,

}



impl Default for SelectModel_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SelectModel_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SelectModel_Request {
  type RmwMsg = super::srv::rmw::SelectModel_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model_name: msg.model_name.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model_name: msg.model_name.to_string(),
    }
  }
}


// Corresponds to human_hand_msgs__srv__SelectModel_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectModel_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub active_model: std::string::String,

}



impl Default for SelectModel_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SelectModel_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SelectModel_Response {
  type RmwMsg = super::srv::rmw::SelectModel_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        success: msg.success,
        message: msg.message.as_str().into(),
        active_model: msg.active_model.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      success: msg.success,
        message: msg.message.as_str().into(),
        active_model: msg.active_model.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      success: msg.success,
      message: msg.message.to_string(),
      active_model: msg.active_model.to_string(),
    }
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


