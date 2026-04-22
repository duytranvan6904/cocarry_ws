# generated from rosidl_generator_py/resource/_idl.py.em
# with input from motoros2_interfaces:msg/InitTrajEnum.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_InitTrajEnum(type):
    """Metaclass of message 'InitTrajEnum'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'INIT_TRAJ_OK': 0,
        'INIT_TRAJ_OK_STR': 'OK',
        'INIT_TRAJ_UNSPECIFIED': 200,
        'INIT_TRAJ_UNSPECIFIED_STR': 'Unspecified failure',
        'INIT_TRAJ_TOO_SMALL': 201,
        'INIT_TRAJ_TOO_SMALL_STR': 'Trajectory must contain at least two points.',
        'INIT_TRAJ_TOO_BIG': 202,
        'INIT_TRAJ_TOO_BIG_STR': 'Trajectory contains too many points (Not enough memory).',
        'INIT_TRAJ_ALREADY_IN_MOTION': 203,
        'INIT_TRAJ_ALREADY_IN_MOTION_STR': 'Already running a trajectory.',
        'INIT_TRAJ_INVALID_STARTING_POS': 204,
        'INIT_TRAJ_INVALID_STARTING_POS_STR': "The first point must match the robot's current position.",
        'INIT_TRAJ_INVALID_VELOCITY': 205,
        'INIT_TRAJ_INVALID_VELOCITY_STR': 'The commanded velocity is too high.',
        'INIT_TRAJ_INVALID_JOINTNAME': 206,
        'INIT_TRAJ_INVALID_JOINTNAME_STR': 'Invalid joint name specified. Check motoros2_config.yaml.',
        'INIT_TRAJ_INCOMPLETE_JOINTLIST': 207,
        'INIT_TRAJ_INCOMPLETE_JOINTLIST_STR': 'Trajectory must contain data for all joints.',
        'INIT_TRAJ_INVALID_TIME': 208,
        'INIT_TRAJ_INVALID_TIME_STR': 'Invalid time in trajectory.',
        'INIT_TRAJ_WRONG_MODE': 209,
        'INIT_TRAJ_WRONG_MODE_STR': 'Must call start_traj_mode service',
        'INIT_TRAJ_BACKWARD_TIME': 210,
        'INIT_TRAJ_BACKWARD_TIME_STR': 'Trajectory message contains waypoints that are not strictly increasing in time.',
        'INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS': 211,
        'INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR': 'Trajectory did not contain position data for all axes.',
        'INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES': 212,
        'INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR': 'Trajectory did not contain velocity data for all axes.',
        'INIT_TRAJ_INVALID_ENDING_VELOCITY': 213,
        'INIT_TRAJ_INVALID_ENDING_VELOCITY_STR': 'The final point in the trajectory must have zero velocity.',
        'INIT_TRAJ_INVALID_ENDING_ACCELERATION': 214,
        'INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR': 'The final point in the trajectory must have zero acceleration.',
        'INIT_TRAJ_DUPLICATE_JOINT_NAME': 215,
        'INIT_TRAJ_DUPLICATE_JOINT_NAME_STR': 'The trajectory contains duplicate joint names.',
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('motoros2_interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'motoros2_interfaces.msg.InitTrajEnum')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__init_traj_enum
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__init_traj_enum
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__init_traj_enum
            cls._TYPE_SUPPORT = module.type_support_msg__msg__init_traj_enum
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__init_traj_enum

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'INIT_TRAJ_OK': cls.__constants['INIT_TRAJ_OK'],
            'INIT_TRAJ_OK_STR': cls.__constants['INIT_TRAJ_OK_STR'],
            'INIT_TRAJ_UNSPECIFIED': cls.__constants['INIT_TRAJ_UNSPECIFIED'],
            'INIT_TRAJ_UNSPECIFIED_STR': cls.__constants['INIT_TRAJ_UNSPECIFIED_STR'],
            'INIT_TRAJ_TOO_SMALL': cls.__constants['INIT_TRAJ_TOO_SMALL'],
            'INIT_TRAJ_TOO_SMALL_STR': cls.__constants['INIT_TRAJ_TOO_SMALL_STR'],
            'INIT_TRAJ_TOO_BIG': cls.__constants['INIT_TRAJ_TOO_BIG'],
            'INIT_TRAJ_TOO_BIG_STR': cls.__constants['INIT_TRAJ_TOO_BIG_STR'],
            'INIT_TRAJ_ALREADY_IN_MOTION': cls.__constants['INIT_TRAJ_ALREADY_IN_MOTION'],
            'INIT_TRAJ_ALREADY_IN_MOTION_STR': cls.__constants['INIT_TRAJ_ALREADY_IN_MOTION_STR'],
            'INIT_TRAJ_INVALID_STARTING_POS': cls.__constants['INIT_TRAJ_INVALID_STARTING_POS'],
            'INIT_TRAJ_INVALID_STARTING_POS_STR': cls.__constants['INIT_TRAJ_INVALID_STARTING_POS_STR'],
            'INIT_TRAJ_INVALID_VELOCITY': cls.__constants['INIT_TRAJ_INVALID_VELOCITY'],
            'INIT_TRAJ_INVALID_VELOCITY_STR': cls.__constants['INIT_TRAJ_INVALID_VELOCITY_STR'],
            'INIT_TRAJ_INVALID_JOINTNAME': cls.__constants['INIT_TRAJ_INVALID_JOINTNAME'],
            'INIT_TRAJ_INVALID_JOINTNAME_STR': cls.__constants['INIT_TRAJ_INVALID_JOINTNAME_STR'],
            'INIT_TRAJ_INCOMPLETE_JOINTLIST': cls.__constants['INIT_TRAJ_INCOMPLETE_JOINTLIST'],
            'INIT_TRAJ_INCOMPLETE_JOINTLIST_STR': cls.__constants['INIT_TRAJ_INCOMPLETE_JOINTLIST_STR'],
            'INIT_TRAJ_INVALID_TIME': cls.__constants['INIT_TRAJ_INVALID_TIME'],
            'INIT_TRAJ_INVALID_TIME_STR': cls.__constants['INIT_TRAJ_INVALID_TIME_STR'],
            'INIT_TRAJ_WRONG_MODE': cls.__constants['INIT_TRAJ_WRONG_MODE'],
            'INIT_TRAJ_WRONG_MODE_STR': cls.__constants['INIT_TRAJ_WRONG_MODE_STR'],
            'INIT_TRAJ_BACKWARD_TIME': cls.__constants['INIT_TRAJ_BACKWARD_TIME'],
            'INIT_TRAJ_BACKWARD_TIME_STR': cls.__constants['INIT_TRAJ_BACKWARD_TIME_STR'],
            'INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS': cls.__constants['INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS'],
            'INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR': cls.__constants['INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR'],
            'INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES': cls.__constants['INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES'],
            'INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR': cls.__constants['INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR'],
            'INIT_TRAJ_INVALID_ENDING_VELOCITY': cls.__constants['INIT_TRAJ_INVALID_ENDING_VELOCITY'],
            'INIT_TRAJ_INVALID_ENDING_VELOCITY_STR': cls.__constants['INIT_TRAJ_INVALID_ENDING_VELOCITY_STR'],
            'INIT_TRAJ_INVALID_ENDING_ACCELERATION': cls.__constants['INIT_TRAJ_INVALID_ENDING_ACCELERATION'],
            'INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR': cls.__constants['INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR'],
            'INIT_TRAJ_DUPLICATE_JOINT_NAME': cls.__constants['INIT_TRAJ_DUPLICATE_JOINT_NAME'],
            'INIT_TRAJ_DUPLICATE_JOINT_NAME_STR': cls.__constants['INIT_TRAJ_DUPLICATE_JOINT_NAME_STR'],
        }

    @property
    def INIT_TRAJ_OK(self):
        """Message constant 'INIT_TRAJ_OK'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_OK']

    @property
    def INIT_TRAJ_OK_STR(self):
        """Message constant 'INIT_TRAJ_OK_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_OK_STR']

    @property
    def INIT_TRAJ_UNSPECIFIED(self):
        """Message constant 'INIT_TRAJ_UNSPECIFIED'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_UNSPECIFIED']

    @property
    def INIT_TRAJ_UNSPECIFIED_STR(self):
        """Message constant 'INIT_TRAJ_UNSPECIFIED_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_UNSPECIFIED_STR']

    @property
    def INIT_TRAJ_TOO_SMALL(self):
        """Message constant 'INIT_TRAJ_TOO_SMALL'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_TOO_SMALL']

    @property
    def INIT_TRAJ_TOO_SMALL_STR(self):
        """Message constant 'INIT_TRAJ_TOO_SMALL_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_TOO_SMALL_STR']

    @property
    def INIT_TRAJ_TOO_BIG(self):
        """Message constant 'INIT_TRAJ_TOO_BIG'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_TOO_BIG']

    @property
    def INIT_TRAJ_TOO_BIG_STR(self):
        """Message constant 'INIT_TRAJ_TOO_BIG_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_TOO_BIG_STR']

    @property
    def INIT_TRAJ_ALREADY_IN_MOTION(self):
        """Message constant 'INIT_TRAJ_ALREADY_IN_MOTION'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_ALREADY_IN_MOTION']

    @property
    def INIT_TRAJ_ALREADY_IN_MOTION_STR(self):
        """Message constant 'INIT_TRAJ_ALREADY_IN_MOTION_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_ALREADY_IN_MOTION_STR']

    @property
    def INIT_TRAJ_INVALID_STARTING_POS(self):
        """Message constant 'INIT_TRAJ_INVALID_STARTING_POS'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_STARTING_POS']

    @property
    def INIT_TRAJ_INVALID_STARTING_POS_STR(self):
        """Message constant 'INIT_TRAJ_INVALID_STARTING_POS_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_STARTING_POS_STR']

    @property
    def INIT_TRAJ_INVALID_VELOCITY(self):
        """Message constant 'INIT_TRAJ_INVALID_VELOCITY'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_VELOCITY']

    @property
    def INIT_TRAJ_INVALID_VELOCITY_STR(self):
        """Message constant 'INIT_TRAJ_INVALID_VELOCITY_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_VELOCITY_STR']

    @property
    def INIT_TRAJ_INVALID_JOINTNAME(self):
        """Message constant 'INIT_TRAJ_INVALID_JOINTNAME'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_JOINTNAME']

    @property
    def INIT_TRAJ_INVALID_JOINTNAME_STR(self):
        """Message constant 'INIT_TRAJ_INVALID_JOINTNAME_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_JOINTNAME_STR']

    @property
    def INIT_TRAJ_INCOMPLETE_JOINTLIST(self):
        """Message constant 'INIT_TRAJ_INCOMPLETE_JOINTLIST'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INCOMPLETE_JOINTLIST']

    @property
    def INIT_TRAJ_INCOMPLETE_JOINTLIST_STR(self):
        """Message constant 'INIT_TRAJ_INCOMPLETE_JOINTLIST_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INCOMPLETE_JOINTLIST_STR']

    @property
    def INIT_TRAJ_INVALID_TIME(self):
        """Message constant 'INIT_TRAJ_INVALID_TIME'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_TIME']

    @property
    def INIT_TRAJ_INVALID_TIME_STR(self):
        """Message constant 'INIT_TRAJ_INVALID_TIME_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_TIME_STR']

    @property
    def INIT_TRAJ_WRONG_MODE(self):
        """Message constant 'INIT_TRAJ_WRONG_MODE'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_WRONG_MODE']

    @property
    def INIT_TRAJ_WRONG_MODE_STR(self):
        """Message constant 'INIT_TRAJ_WRONG_MODE_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_WRONG_MODE_STR']

    @property
    def INIT_TRAJ_BACKWARD_TIME(self):
        """Message constant 'INIT_TRAJ_BACKWARD_TIME'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_BACKWARD_TIME']

    @property
    def INIT_TRAJ_BACKWARD_TIME_STR(self):
        """Message constant 'INIT_TRAJ_BACKWARD_TIME_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_BACKWARD_TIME_STR']

    @property
    def INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS(self):
        """Message constant 'INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS']

    @property
    def INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR(self):
        """Message constant 'INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR']

    @property
    def INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES(self):
        """Message constant 'INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES']

    @property
    def INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR(self):
        """Message constant 'INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR']

    @property
    def INIT_TRAJ_INVALID_ENDING_VELOCITY(self):
        """Message constant 'INIT_TRAJ_INVALID_ENDING_VELOCITY'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_ENDING_VELOCITY']

    @property
    def INIT_TRAJ_INVALID_ENDING_VELOCITY_STR(self):
        """Message constant 'INIT_TRAJ_INVALID_ENDING_VELOCITY_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_ENDING_VELOCITY_STR']

    @property
    def INIT_TRAJ_INVALID_ENDING_ACCELERATION(self):
        """Message constant 'INIT_TRAJ_INVALID_ENDING_ACCELERATION'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_ENDING_ACCELERATION']

    @property
    def INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR(self):
        """Message constant 'INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR']

    @property
    def INIT_TRAJ_DUPLICATE_JOINT_NAME(self):
        """Message constant 'INIT_TRAJ_DUPLICATE_JOINT_NAME'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_DUPLICATE_JOINT_NAME']

    @property
    def INIT_TRAJ_DUPLICATE_JOINT_NAME_STR(self):
        """Message constant 'INIT_TRAJ_DUPLICATE_JOINT_NAME_STR'."""
        return Metaclass_InitTrajEnum.__constants['INIT_TRAJ_DUPLICATE_JOINT_NAME_STR']


class InitTrajEnum(metaclass=Metaclass_InitTrajEnum):
    """
    Message class 'InitTrajEnum'.

    Constants:
      INIT_TRAJ_OK
      INIT_TRAJ_OK_STR
      INIT_TRAJ_UNSPECIFIED
      INIT_TRAJ_UNSPECIFIED_STR
      INIT_TRAJ_TOO_SMALL
      INIT_TRAJ_TOO_SMALL_STR
      INIT_TRAJ_TOO_BIG
      INIT_TRAJ_TOO_BIG_STR
      INIT_TRAJ_ALREADY_IN_MOTION
      INIT_TRAJ_ALREADY_IN_MOTION_STR
      INIT_TRAJ_INVALID_STARTING_POS
      INIT_TRAJ_INVALID_STARTING_POS_STR
      INIT_TRAJ_INVALID_VELOCITY
      INIT_TRAJ_INVALID_VELOCITY_STR
      INIT_TRAJ_INVALID_JOINTNAME
      INIT_TRAJ_INVALID_JOINTNAME_STR
      INIT_TRAJ_INCOMPLETE_JOINTLIST
      INIT_TRAJ_INCOMPLETE_JOINTLIST_STR
      INIT_TRAJ_INVALID_TIME
      INIT_TRAJ_INVALID_TIME_STR
      INIT_TRAJ_WRONG_MODE
      INIT_TRAJ_WRONG_MODE_STR
      INIT_TRAJ_BACKWARD_TIME
      INIT_TRAJ_BACKWARD_TIME_STR
      INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS
      INIT_TRAJ_WRONG_NUMBER_OF_POSITIONS_STR
      INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES
      INIT_TRAJ_WRONG_NUMBER_OF_VELOCITIES_STR
      INIT_TRAJ_INVALID_ENDING_VELOCITY
      INIT_TRAJ_INVALID_ENDING_VELOCITY_STR
      INIT_TRAJ_INVALID_ENDING_ACCELERATION
      INIT_TRAJ_INVALID_ENDING_ACCELERATION_STR
      INIT_TRAJ_DUPLICATE_JOINT_NAME
      INIT_TRAJ_DUPLICATE_JOINT_NAME_STR
    """

    __slots__ = [
        '_value',
    ]

    _fields_and_field_types = {
        'value': 'uint16',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint16'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.value = kwargs.get('value', int())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.value != other.value:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def value(self):
        """Message field 'value'."""
        return self._value

    @value.setter
    def value(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'value' field must be of type 'int'"
            assert value >= 0 and value < 65536, \
                "The 'value' field must be an unsigned integer in [0, 65535]"
        self._value = value
