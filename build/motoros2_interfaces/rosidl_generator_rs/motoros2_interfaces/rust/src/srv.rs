#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};




// Corresponds to motoros2_interfaces__srv__GetActiveAlarmInfo_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetActiveAlarmInfo_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for GetActiveAlarmInfo_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetActiveAlarmInfo_Request::default())
  }
}

impl rosidl_runtime_rs::Message for GetActiveAlarmInfo_Request {
  type RmwMsg = super::srv::rmw::GetActiveAlarmInfo_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__GetActiveAlarmInfo_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct GetActiveAlarmInfo_Response {
    /// Result of the service invocation. Values other than one (1) signal failure.
    ///
    /// NOTE: future versions of this service may use a different set of result codes
    pub result_code: u32,

    /// string representation of the value in 'result_code', for humans
    pub result_message: std::string::String,

    /// Each entry in this list provides detailed information about all currently
    /// active alarms. If this list is empty, there are no active alarms.
    ///
    /// Note: order of entries in this list does not encode for any specific severity
    /// or priority of active alarms.
    pub alarms: Vec<super::msg::AlarmInfo>,

    /// Each entry in this list provides detailed information about all currently
    /// active errors. If this list is empty, there are no active errors.
    ///
    /// Note: order of entries in this list does not encode for any specific severity
    /// or priority of active errors.
    pub errors: Vec<super::msg::ErrorInfo>,

}



impl Default for GetActiveAlarmInfo_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::GetActiveAlarmInfo_Response::default())
  }
}

impl rosidl_runtime_rs::Message for GetActiveAlarmInfo_Response {
  type RmwMsg = super::srv::rmw::GetActiveAlarmInfo_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        result_message: msg.result_message.as_str().into(),
        alarms: msg.alarms
          .into_iter()
          .map(|elem| super::msg::AlarmInfo::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
        errors: msg.errors
          .into_iter()
          .map(|elem| super::msg::ErrorInfo::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        result_message: msg.result_message.as_str().into(),
        alarms: msg.alarms
          .iter()
          .map(|elem| super::msg::AlarmInfo::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
        errors: msg.errors
          .iter()
          .map(|elem| super::msg::ErrorInfo::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      result_message: msg.result_message.to_string(),
      alarms: msg.alarms
          .into_iter()
          .map(super::msg::AlarmInfo::from_rmw_message)
          .collect(),
      errors: msg.errors
          .into_iter()
          .map(super::msg::ErrorInfo::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ListInformJobs_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ListInformJobs_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ListInformJobs_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ListInformJobs_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ListInformJobs_Request {
  type RmwMsg = super::srv::rmw::ListInformJobs_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ListInformJobs_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    pub message: std::string::String,

    /// The list of jobs present on the controller.
    ///
    /// NOTE:
    /// - these are job names, not filenames, and thus will not include the file
    ///   extension (JBI)
    /// - character encodings other than ASCII are only partially supported
    pub names: Vec<std::string::String>,

}



impl Default for ListInformJobs_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ListInformJobs_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ListInformJobs_Response {
  type RmwMsg = super::srv::rmw::ListInformJobs_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        names: msg.names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
        names: msg.names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      message: msg.message.to_string(),
      names: msg.names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
    }
  }
}


// Corresponds to motoros2_interfaces__srv__QueueTrajPoint_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QueueTrajPoint_Request {
    /// Submit a trajectory point to the continuous motion queue.
    ///
    /// The start_point_queue_mode service must have been invoked first
    pub joint_names: Vec<std::string::String>,


    // This member is not documented.
    #[allow(missing_docs)]
    pub point: trajectory_msgs::msg::JointTrajectoryPoint,

}



impl Default for QueueTrajPoint_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::QueueTrajPoint_Request::default())
  }
}

impl rosidl_runtime_rs::Message for QueueTrajPoint_Request {
  type RmwMsg = super::srv::rmw::QueueTrajPoint_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        point: trajectory_msgs::msg::JointTrajectoryPoint::into_rmw_message(std::borrow::Cow::Owned(msg.point)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        joint_names: msg.joint_names
          .iter()
          .map(|elem| elem.as_str().into())
          .collect(),
        point: trajectory_msgs::msg::JointTrajectoryPoint::into_rmw_message(std::borrow::Cow::Borrowed(&msg.point)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      joint_names: msg.joint_names
          .into_iter()
          .map(|elem| elem.to_string())
          .collect(),
      point: trajectory_msgs::msg::JointTrajectoryPoint::from_rmw_message(msg.point),
    }
  }
}


// Corresponds to motoros2_interfaces__srv__QueueTrajPoint_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct QueueTrajPoint_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::msg::QueueResultEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: std::string::String,

}



impl Default for QueueTrajPoint_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::QueueTrajPoint_Response::default())
  }
}

impl rosidl_runtime_rs::Message for QueueTrajPoint_Response {
  type RmwMsg = super::srv::rmw::QueueTrajPoint_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::QueueResultEnum::into_rmw_message(std::borrow::Cow::Owned(msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::QueueResultEnum::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: super::msg::QueueResultEnum::from_rmw_message(msg.result_code),
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ReadMRegister_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadMRegister_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ReadMRegister_Request {
  type RmwMsg = super::srv::rmw::ReadMRegister_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ReadMRegister_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadMRegister_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u16,

}



impl Default for ReadMRegister_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadMRegister_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ReadMRegister_Response {
  type RmwMsg = super::srv::rmw::ReadMRegister_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      message: msg.message.to_string(),
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ReadSingleIO_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadSingleIO_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ReadSingleIO_Request {
  type RmwMsg = super::srv::rmw::ReadSingleIO_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ReadSingleIO_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadSingleIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: i32,

}



impl Default for ReadSingleIO_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadSingleIO_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ReadSingleIO_Response {
  type RmwMsg = super::srv::rmw::ReadSingleIO_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      message: msg.message.to_string(),
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ReadGroupIO_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadGroupIO_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ReadGroupIO_Request {
  type RmwMsg = super::srv::rmw::ReadGroupIO_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ReadGroupIO_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ReadGroupIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,


    // This member is not documented.
    #[allow(missing_docs)]
    pub value: u8,

}



impl Default for ReadGroupIO_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ReadGroupIO_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ReadGroupIO_Response {
  type RmwMsg = super::srv::rmw::ReadGroupIO_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        success: msg.success,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
      success: msg.success,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      message: msg.message.to_string(),
      success: msg.success,
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ResetError_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ResetError_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for ResetError_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ResetError_Request::default())
  }
}

impl rosidl_runtime_rs::Message for ResetError_Request {
  type RmwMsg = super::srv::rmw::ResetError_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__ResetError_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ResetError_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::msg::MotionReadyEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: std::string::String,

}



impl Default for ResetError_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::ResetError_Response::default())
  }
}

impl rosidl_runtime_rs::Message for ResetError_Response {
  type RmwMsg = super::srv::rmw::ResetError_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::MotionReadyEnum::into_rmw_message(std::borrow::Cow::Owned(msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::MotionReadyEnum::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: super::msg::MotionReadyEnum::from_rmw_message(msg.result_code),
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to motoros2_interfaces__srv__SelectMotionTool_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SelectMotionTool_Request::default())
  }
}

impl rosidl_runtime_rs::Message for SelectMotionTool_Request {
  type RmwMsg = super::srv::rmw::SelectMotionTool_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        group_number: msg.group_number,
        tool_number: msg.tool_number,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      group_number: msg.group_number,
      tool_number: msg.tool_number,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      group_number: msg.group_number,
      tool_number: msg.tool_number,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__SelectMotionTool_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SelectMotionTool_Response {
    /// Result of the service invocation. Values other than zero (0) signal failure.
    ///
    /// Refer to SelectionResultCodes.msg for defined values
    pub result_code: super::msg::SelectionResultCodes,

    /// A human-readable error message, or an empty string if there was no error.
    pub message: std::string::String,

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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::SelectMotionTool_Response::default())
  }
}

impl rosidl_runtime_rs::Message for SelectMotionTool_Response {
  type RmwMsg = super::srv::rmw::SelectMotionTool_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::SelectionResultCodes::into_rmw_message(std::borrow::Cow::Owned(msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::SelectionResultCodes::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: super::msg::SelectionResultCodes::from_rmw_message(msg.result_code),
      message: msg.message.to_string(),
      success: msg.success,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__StartTrajMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartTrajMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for StartTrajMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StartTrajMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for StartTrajMode_Request {
  type RmwMsg = super::srv::rmw::StartTrajMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__StartTrajMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartTrajMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::msg::MotionReadyEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: std::string::String,

}



impl Default for StartTrajMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StartTrajMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for StartTrajMode_Response {
  type RmwMsg = super::srv::rmw::StartTrajMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::MotionReadyEnum::into_rmw_message(std::borrow::Cow::Owned(msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::MotionReadyEnum::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: super::msg::MotionReadyEnum::from_rmw_message(msg.result_code),
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to motoros2_interfaces__srv__StartPointQueueMode_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartPointQueueMode_Request {

    // This member is not documented.
    #[allow(missing_docs)]
    pub structure_needs_at_least_one_member: u8,

}



impl Default for StartPointQueueMode_Request {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StartPointQueueMode_Request::default())
  }
}

impl rosidl_runtime_rs::Message for StartPointQueueMode_Request {
  type RmwMsg = super::srv::rmw::StartPointQueueMode_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      structure_needs_at_least_one_member: msg.structure_needs_at_least_one_member,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__StartPointQueueMode_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct StartPointQueueMode_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: super::msg::MotionReadyEnum,

    /// string representation of the value in 'result_code', for humans
    pub message: std::string::String,

}



impl Default for StartPointQueueMode_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::StartPointQueueMode_Response::default())
  }
}

impl rosidl_runtime_rs::Message for StartPointQueueMode_Response {
  type RmwMsg = super::srv::rmw::StartPointQueueMode_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::MotionReadyEnum::into_rmw_message(std::borrow::Cow::Owned(msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: super::msg::MotionReadyEnum::into_rmw_message(std::borrow::Cow::Borrowed(&msg.result_code)).into_owned(),
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: super::msg::MotionReadyEnum::from_rmw_message(msg.result_code),
      message: msg.message.to_string(),
    }
  }
}


// Corresponds to motoros2_interfaces__srv__WriteMRegister_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteMRegister_Request::default())
  }
}

impl rosidl_runtime_rs::Message for WriteMRegister_Request {
  type RmwMsg = super::srv::rmw::WriteMRegister_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__WriteMRegister_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteMRegister_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for WriteMRegister_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteMRegister_Response::default())
  }
}

impl rosidl_runtime_rs::Message for WriteMRegister_Response {
  type RmwMsg = super::srv::rmw::WriteMRegister_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      message: msg.message.to_string(),
      success: msg.success,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__WriteSingleIO_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteSingleIO_Request::default())
  }
}

impl rosidl_runtime_rs::Message for WriteSingleIO_Request {
  type RmwMsg = super::srv::rmw::WriteSingleIO_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__WriteSingleIO_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteSingleIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for WriteSingleIO_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteSingleIO_Response::default())
  }
}

impl rosidl_runtime_rs::Message for WriteSingleIO_Response {
  type RmwMsg = super::srv::rmw::WriteSingleIO_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      message: msg.message.to_string(),
      success: msg.success,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__WriteGroupIO_Request

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteGroupIO_Request::default())
  }
}

impl rosidl_runtime_rs::Message for WriteGroupIO_Request {
  type RmwMsg = super::srv::rmw::WriteGroupIO_Request;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        address: msg.address,
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      address: msg.address,
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      address: msg.address,
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__srv__WriteGroupIO_Response

// This struct is not documented.
#[allow(missing_docs)]

#[allow(non_camel_case_types)]
#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct WriteGroupIO_Response {

    // This member is not documented.
    #[allow(missing_docs)]
    pub result_code: u32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub success: bool,

}



impl Default for WriteGroupIO_Response {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::srv::rmw::WriteGroupIO_Response::default())
  }
}

impl rosidl_runtime_rs::Message for WriteGroupIO_Response {
  type RmwMsg = super::srv::rmw::WriteGroupIO_Response;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        result_code: msg.result_code,
        message: msg.message.as_str().into(),
        success: msg.success,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      result_code: msg.result_code,
        message: msg.message.as_str().into(),
      success: msg.success,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      result_code: msg.result_code,
      message: msg.message.to_string(),
      success: msg.success,
    }
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


