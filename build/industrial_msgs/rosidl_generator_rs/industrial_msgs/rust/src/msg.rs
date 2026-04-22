#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to industrial_msgs__msg__DebugLevel
/// Debug level message enumeration.  This may replicate some functionality that
/// alreay exists in the ROS logger.
/// TODO: Get more information on the ROS Logger.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DebugLevel::default())
  }
}

impl rosidl_runtime_rs::Message for DebugLevel {
  type RmwMsg = super::msg::rmw::DebugLevel;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        val: msg.val,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      val: msg.val,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      val: msg.val,
    }
  }
}


// Corresponds to industrial_msgs__msg__DeviceInfo
/// Device info captures device agnostic information about a piece of hardware.
/// This message is meant as a generic as possible.  Items that don't apply should
/// be left blank.  This message is not meant to replace diagnostic messages, but
/// rather provide a standard service message that can be used to populate standard
/// components (like a GUI for example)

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct DeviceInfo {

    // This member is not documented.
    #[allow(missing_docs)]
    pub model: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub serial_number: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub hw_version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub sw_version: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub address: std::string::String,

}



impl Default for DeviceInfo {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::DeviceInfo::default())
  }
}

impl rosidl_runtime_rs::Message for DeviceInfo {
  type RmwMsg = super::msg::rmw::DeviceInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model: msg.model.as_str().into(),
        serial_number: msg.serial_number.as_str().into(),
        hw_version: msg.hw_version.as_str().into(),
        sw_version: msg.sw_version.as_str().into(),
        address: msg.address.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        model: msg.model.as_str().into(),
        serial_number: msg.serial_number.as_str().into(),
        hw_version: msg.hw_version.as_str().into(),
        sw_version: msg.sw_version.as_str().into(),
        address: msg.address.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      model: msg.model.to_string(),
      serial_number: msg.serial_number.to_string(),
      hw_version: msg.hw_version.to_string(),
      sw_version: msg.sw_version.to_string(),
      address: msg.address.to_string(),
    }
  }
}


// Corresponds to industrial_msgs__msg__RobotMode
/// The Robot mode message encapsulates the mode/teach state of the robot
/// Typically this is controlled by the pendant key switch, but not always

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotMode::default())
  }
}

impl rosidl_runtime_rs::Message for RobotMode {
  type RmwMsg = super::msg::rmw::RobotMode;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        val: msg.val,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      val: msg.val,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      val: msg.val,
    }
  }
}


// Corresponds to industrial_msgs__msg__RobotStatus
/// The RobotStatus message contains low level status information 
/// that is specific to an industrial robot controller

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct RobotStatus {
    /// The header frame ID is not used
    pub header: std_msgs::msg::Header,

    /// The robot mode captures the operating mode of the robot.  When in
    /// manual, remote motion is not possible.
    pub mode: super::msg::RobotMode,

    /// Estop status: True if robot is e-stopped.  The drives are disabled
    /// and motion is not possible.  The e-stop condition must be acknowledged
    /// and cleared before any motion can begin.
    pub e_stopped: super::msg::TriState,

    /// Drive power status: True if drives are powered.  Motion commands will
    /// automatically enable the drives if required.  Drive power is not requred
    /// for possible motion
    pub drives_powered: super::msg::TriState,

    /// Motion enabled: True if robot motion is possible.
    pub motion_possible: super::msg::TriState,

    /// Motion status: True if robot is in motion, otherwise false
    pub in_motion: super::msg::TriState,

    /// Error status: True if there is an error condition on the robot. Motion may
    /// or may not be affected (see motion_possible)
    pub in_error: super::msg::TriState,

    /// Error code: Vendor specific error codes. If this list is empty, there are
    /// no active errors on the controller. Order of entries in this list does
    /// not necessarily encode for any specific severity or priority of active
    /// errors.
    pub error_codes: Vec<i32>,

}



impl Default for RobotStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::RobotStatus::default())
  }
}

impl rosidl_runtime_rs::Message for RobotStatus {
  type RmwMsg = super::msg::rmw::RobotStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        mode: super::msg::RobotMode::into_rmw_message(std::borrow::Cow::Owned(msg.mode)).into_owned(),
        e_stopped: super::msg::TriState::into_rmw_message(std::borrow::Cow::Owned(msg.e_stopped)).into_owned(),
        drives_powered: super::msg::TriState::into_rmw_message(std::borrow::Cow::Owned(msg.drives_powered)).into_owned(),
        motion_possible: super::msg::TriState::into_rmw_message(std::borrow::Cow::Owned(msg.motion_possible)).into_owned(),
        in_motion: super::msg::TriState::into_rmw_message(std::borrow::Cow::Owned(msg.in_motion)).into_owned(),
        in_error: super::msg::TriState::into_rmw_message(std::borrow::Cow::Owned(msg.in_error)).into_owned(),
        error_codes: msg.error_codes.into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        mode: super::msg::RobotMode::into_rmw_message(std::borrow::Cow::Borrowed(&msg.mode)).into_owned(),
        e_stopped: super::msg::TriState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.e_stopped)).into_owned(),
        drives_powered: super::msg::TriState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.drives_powered)).into_owned(),
        motion_possible: super::msg::TriState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.motion_possible)).into_owned(),
        in_motion: super::msg::TriState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.in_motion)).into_owned(),
        in_error: super::msg::TriState::into_rmw_message(std::borrow::Cow::Borrowed(&msg.in_error)).into_owned(),
        error_codes: msg.error_codes.as_slice().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      mode: super::msg::RobotMode::from_rmw_message(msg.mode),
      e_stopped: super::msg::TriState::from_rmw_message(msg.e_stopped),
      drives_powered: super::msg::TriState::from_rmw_message(msg.drives_powered),
      motion_possible: super::msg::TriState::from_rmw_message(msg.motion_possible),
      in_motion: super::msg::TriState::from_rmw_message(msg.in_motion),
      in_error: super::msg::TriState::from_rmw_message(msg.in_error),
      error_codes: msg.error_codes
          .into_iter()
          .collect(),
    }
  }
}


// Corresponds to industrial_msgs__msg__ServiceReturnCode
/// Service return codes for simple requests.  All ROS-Industrial service
/// replies are required to have a return code indicating success or failure
/// Specific return codes for different failure should be negative.

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ServiceReturnCode::default())
  }
}

impl rosidl_runtime_rs::Message for ServiceReturnCode {
  type RmwMsg = super::msg::rmw::ServiceReturnCode;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        val: msg.val,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      val: msg.val,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      val: msg.val,
    }
  }
}


// Corresponds to industrial_msgs__msg__TriState
/// The tri-state captures boolean values with the additional state of unknown

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::TriState::default())
  }
}

impl rosidl_runtime_rs::Message for TriState {
  type RmwMsg = super::msg::rmw::TriState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        val: msg.val,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      val: msg.val,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      val: msg.val,
    }
  }
}


