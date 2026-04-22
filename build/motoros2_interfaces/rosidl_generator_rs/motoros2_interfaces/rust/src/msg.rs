#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to motoros2_interfaces__msg__AlarmInfo
/// SPDX-FileCopyrightText: 2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlarmInfo {
    /// Alarm Number
    pub number: u32,

    /// Alarm Name/Message
    pub message: std::string::String,

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
    pub datetime: builtin_interfaces::msg::Time,

    /// reserved for future use: contents (from CSV)
    pub contents: std::string::String,

    /// reserved for future use: meaning (from CSV)
    pub description: std::string::String,

    /// reserved for future use: potential causes and their potential remedies (from CSV)
    pub help: Vec<super::msg::AlarmCauseRemedy>,

}



impl Default for AlarmInfo {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AlarmInfo::default())
  }
}

impl rosidl_runtime_rs::Message for AlarmInfo {
  type RmwMsg = super::msg::rmw::AlarmInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        number: msg.number,
        message: msg.message.as_str().into(),
        sub_code: msg.sub_code,
        datetime: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.datetime)).into_owned(),
        contents: msg.contents.as_str().into(),
        description: msg.description.as_str().into(),
        help: msg.help
          .into_iter()
          .map(|elem| super::msg::AlarmCauseRemedy::into_rmw_message(std::borrow::Cow::Owned(elem)).into_owned())
          .collect(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      number: msg.number,
        message: msg.message.as_str().into(),
      sub_code: msg.sub_code,
        datetime: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.datetime)).into_owned(),
        contents: msg.contents.as_str().into(),
        description: msg.description.as_str().into(),
        help: msg.help
          .iter()
          .map(|elem| super::msg::AlarmCauseRemedy::into_rmw_message(std::borrow::Cow::Borrowed(elem)).into_owned())
          .collect(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      number: msg.number,
      message: msg.message.to_string(),
      sub_code: msg.sub_code,
      datetime: builtin_interfaces::msg::Time::from_rmw_message(msg.datetime),
      contents: msg.contents.to_string(),
      description: msg.description.to_string(),
      help: msg.help
          .into_iter()
          .map(super::msg::AlarmCauseRemedy::from_rmw_message)
          .collect(),
    }
  }
}


// Corresponds to motoros2_interfaces__msg__AlarmCauseRemedy
/// SPDX-FileCopyrightText: 2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct AlarmCauseRemedy {
    /// Cause
    pub cause: std::string::String,

    /// Remedy
    pub remedy: std::string::String,

}



impl Default for AlarmCauseRemedy {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::AlarmCauseRemedy::default())
  }
}

impl rosidl_runtime_rs::Message for AlarmCauseRemedy {
  type RmwMsg = super::msg::rmw::AlarmCauseRemedy;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        cause: msg.cause.as_str().into(),
        remedy: msg.remedy.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        cause: msg.cause.as_str().into(),
        remedy: msg.remedy.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      cause: msg.cause.to_string(),
      remedy: msg.remedy.to_string(),
    }
  }
}


// Corresponds to motoros2_interfaces__msg__ErrorInfo
/// SPDX-FileCopyrightText: 2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct ErrorInfo {
    /// Error Number
    pub number: u32,

    /// Error Name/Message
    pub message: std::string::String,

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
    pub datetime: builtin_interfaces::msg::Time,

}



impl Default for ErrorInfo {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::ErrorInfo::default())
  }
}

impl rosidl_runtime_rs::Message for ErrorInfo {
  type RmwMsg = super::msg::rmw::ErrorInfo;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        number: msg.number,
        message: msg.message.as_str().into(),
        sub_code: msg.sub_code,
        datetime: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Owned(msg.datetime)).into_owned(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      number: msg.number,
        message: msg.message.as_str().into(),
      sub_code: msg.sub_code,
        datetime: builtin_interfaces::msg::Time::into_rmw_message(std::borrow::Cow::Borrowed(&msg.datetime)).into_owned(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      number: msg.number,
      message: msg.message.to_string(),
      sub_code: msg.sub_code,
      datetime: builtin_interfaces::msg::Time::from_rmw_message(msg.datetime),
    }
  }
}


// Corresponds to motoros2_interfaces__msg__InformJobCrudResultCodes
/// SPDX-FileCopyrightText: 2024, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2024, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::InformJobCrudResultCodes::default())
  }
}

impl rosidl_runtime_rs::Message for InformJobCrudResultCodes {
  type RmwMsg = super::msg::rmw::InformJobCrudResultCodes;

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


// Corresponds to motoros2_interfaces__msg__InitTrajEnum
/// SPDX-FileCopyrightText: 2024, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2024, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::InitTrajEnum::default())
  }
}

impl rosidl_runtime_rs::Message for InitTrajEnum {
  type RmwMsg = super::msg::rmw::InitTrajEnum;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__msg__IoResultCodes
/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::IoResultCodes::default())
  }
}

impl rosidl_runtime_rs::Message for IoResultCodes {
  type RmwMsg = super::msg::rmw::IoResultCodes;

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


// Corresponds to motoros2_interfaces__msg__MotionReadyEnum
/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::MotionReadyEnum::default())
  }
}

impl rosidl_runtime_rs::Message for MotionReadyEnum {
  type RmwMsg = super::msg::rmw::MotionReadyEnum;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__msg__QueueResultEnum
/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::QueueResultEnum::default())
  }
}

impl rosidl_runtime_rs::Message for QueueResultEnum {
  type RmwMsg = super::msg::rmw::QueueResultEnum;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
    }
  }
}


// Corresponds to motoros2_interfaces__msg__SelectionResultCodes
/// SPDX-FileCopyrightText: 2022-2023, Yaskawa America, Inc.
/// SPDX-FileCopyrightText: 2022-2023, Delft University of Technology
///
/// SPDX-License-Identifier: Apache-2.0

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
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
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SelectionResultCodes::default())
  }
}

impl rosidl_runtime_rs::Message for SelectionResultCodes {
  type RmwMsg = super::msg::rmw::SelectionResultCodes;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        value: msg.value,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
      value: msg.value,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      value: msg.value,
    }
  }
}


