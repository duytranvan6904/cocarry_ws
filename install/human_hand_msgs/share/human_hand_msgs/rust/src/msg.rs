#[cfg(feature = "serde")]
use serde::{Deserialize, Serialize};



// Corresponds to human_hand_msgs__msg__HandState
/// Measured hand position from camera (world frame, post-calibration)

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct HandState {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


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
    pub source: std::string::String,

}



impl Default for HandState {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::HandState::default())
  }
}

impl rosidl_runtime_rs::Message for HandState {
  type RmwMsg = super::msg::rmw::HandState;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        x: msg.x,
        y: msg.y,
        z: msg.z,
        tracking_id: msg.tracking_id,
        is_tracked: msg.is_tracked,
        confidence: msg.confidence,
        source: msg.source.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      x: msg.x,
      y: msg.y,
      z: msg.z,
      tracking_id: msg.tracking_id,
      is_tracked: msg.is_tracked,
      confidence: msg.confidence,
        source: msg.source.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      x: msg.x,
      y: msg.y,
      z: msg.z,
      tracking_id: msg.tracking_id,
      is_tracked: msg.is_tracked,
      confidence: msg.confidence,
      source: msg.source.to_string(),
    }
  }
}


// Corresponds to human_hand_msgs__msg__HandPrediction
/// Predicted next hand position from ML model

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct HandPrediction {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


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
    pub model_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub buffer_size: i32,


    // This member is not documented.
    #[allow(missing_docs)]
    pub prediction_confidence: f64,

}



impl Default for HandPrediction {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::HandPrediction::default())
  }
}

impl rosidl_runtime_rs::Message for HandPrediction {
  type RmwMsg = super::msg::rmw::HandPrediction;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        x: msg.x,
        y: msg.y,
        z: msg.z,
        inference_time_ms: msg.inference_time_ms,
        model_name: msg.model_name.as_str().into(),
        buffer_size: msg.buffer_size,
        prediction_confidence: msg.prediction_confidence,
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
      x: msg.x,
      y: msg.y,
      z: msg.z,
      inference_time_ms: msg.inference_time_ms,
        model_name: msg.model_name.as_str().into(),
      buffer_size: msg.buffer_size,
      prediction_confidence: msg.prediction_confidence,
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      x: msg.x,
      y: msg.y,
      z: msg.z,
      inference_time_ms: msg.inference_time_ms,
      model_name: msg.model_name.to_string(),
      buffer_size: msg.buffer_size,
      prediction_confidence: msg.prediction_confidence,
    }
  }
}


// Corresponds to human_hand_msgs__msg__SystemStatus
/// System monitoring status

#[cfg_attr(feature = "serde", derive(Deserialize, Serialize))]
#[derive(Clone, Debug, PartialEq, PartialOrd)]
pub struct SystemStatus {

    // This member is not documented.
    #[allow(missing_docs)]
    pub header: std_msgs::msg::Header,


    // This member is not documented.
    #[allow(missing_docs)]
    pub node_name: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub status: std::string::String,


    // This member is not documented.
    #[allow(missing_docs)]
    pub fps: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub latency_ms: f64,


    // This member is not documented.
    #[allow(missing_docs)]
    pub message: std::string::String,

}



impl Default for SystemStatus {
  fn default() -> Self {
    <Self as rosidl_runtime_rs::Message>::from_rmw_message(super::msg::rmw::SystemStatus::default())
  }
}

impl rosidl_runtime_rs::Message for SystemStatus {
  type RmwMsg = super::msg::rmw::SystemStatus;

  fn into_rmw_message(msg_cow: std::borrow::Cow<'_, Self>) -> std::borrow::Cow<'_, Self::RmwMsg> {
    match msg_cow {
      std::borrow::Cow::Owned(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Owned(msg.header)).into_owned(),
        node_name: msg.node_name.as_str().into(),
        status: msg.status.as_str().into(),
        fps: msg.fps,
        latency_ms: msg.latency_ms,
        message: msg.message.as_str().into(),
      }),
      std::borrow::Cow::Borrowed(msg) => std::borrow::Cow::Owned(Self::RmwMsg {
        header: std_msgs::msg::Header::into_rmw_message(std::borrow::Cow::Borrowed(&msg.header)).into_owned(),
        node_name: msg.node_name.as_str().into(),
        status: msg.status.as_str().into(),
      fps: msg.fps,
      latency_ms: msg.latency_ms,
        message: msg.message.as_str().into(),
      })
    }
  }

  fn from_rmw_message(msg: Self::RmwMsg) -> Self {
    Self {
      header: std_msgs::msg::Header::from_rmw_message(msg.header),
      node_name: msg.node_name.to_string(),
      status: msg.status.to_string(),
      fps: msg.fps,
      latency_ms: msg.latency_ms,
      message: msg.message.to_string(),
    }
  }
}


