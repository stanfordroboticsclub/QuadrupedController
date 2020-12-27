import numpy as np
from enum import Enum
import yaml
from dataclasses import dataclass


@dataclass
class Configuration:
    ps4_color: dict
    ps4_deactivated_color: dict

    #################### COMMANDS ####################
    max_x_velocity: float  # maximum forward/back velocity [m/s]
    max_y_velocity: float  # maximum sideways velocity [m/s]
    max_yaw_rate: float  # maximum yaw rate [rad/s]
    max_pitch: float  # maximum pitch angle [rad]

    #################### MOVEMENT PARAMS ####################
    z_time_constant: float  # 1st order time constant on raising/lowering the robot [s]
    z_speed: float  # maximum speed [m/s]
    pitch_deadband: float  # [joystick deadband]
    pitch_time_constant: float  # smoothing constant on pitching [s]
    max_pitch_rate: float  # max pitch rate [rad/s]
    roll_speed: float  # maximum roll rate [rad/s]
    yaw_time_constant: float  # 1st order time constant on yaw movement [s]
    max_stance_yaw: float  # maximum yawing angle [rad]
    max_stance_yaw_rate: float  # maximum yawing rate [rad/s]

    #################### STANCE ####################
    delta_x: float  # 1/2 the distance between the front and back sets of feet [m]
    delta_y: float  # 1/2 the distance between the left and right sets of feet [m]
    x_shift: float  # shift the feet forward and backward relative to center [m]
    default_z_ref: float  # default standing height of the robot (negative b/c legs go underneath the robot) [m]

    #################### SWING ######################
    z_clearance: float
    alpha: float  # Ratio between touchdown distance and total horizontal stance movement
    beta: float  # Ratio between touchdown distance and total horizontal stance movement

    #################### GAIT #######################
    overlap_time: float  # duration of the phase where all four feet are on the ground
    swing_time: float  # duration of the phase when only two feet are on the ground
    num_phases: int  # Number of discrete phases during one gait cycle
    contact_phases: np.ndarray  # ndarray of shape (4, num_phases). 1 = stance, 0 = swing.

    #################### IMPLEMENTATION PARAMS ###################
    dt: float = 0.01  # time delta between calculating new position commands [s]

    @classmethod
    def from_yaml(cls, yaml_file):
        """Creates a new Configuration from parameters specified in a YAML file.

        Will raise TypeErrors if the yaml does not contain all the
        required parameters or if it contains invalid parameters.

        Args:
            yaml_file (string): Filepath

        Returns:
            Configuration: Configuration object made from the yaml file.
        """
        with open(yaml_file) as f:
            yaml_config = yaml.safe_load(f)
            config = Configuration(**yaml_config)

            # Manually convert the yaml lists into ndarrays
            config.contact_phases = np.array(config.contact_phases)
            return config

    @property
    def default_stance(self):
        return np.array(
            [
                [
                    self.delta_x + self.x_shift,
                    self.delta_x + self.x_shift,
                    -self.delta_x + self.x_shift,
                    -self.delta_x + self.x_shift,
                ],
                [-self.delta_y, self.delta_y, -self.delta_y, self.delta_y],
                [0, 0, 0, 0],
            ]
        )

    ########################### GAIT ####################
    @property
    def overlap_ticks(self):
        return self.overlap_time // self.dt

    @property
    def swing_ticks(self):
        return self.swing_time // self.dt

    @property
    def stance_ticks(self):
        return 2 * self.overlap_ticks + self.swing_ticks

    @property
    def phase_ticks(self):
        return np.array(
            [self.overlap_ticks, self.swing_ticks, self.overlap_ticks, self.swing_ticks]
        )

    @property
    def phase_length(self):
        return 2 * self.overlap_ticks + 2 * self.swing_ticks
