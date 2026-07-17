import cv2
import numpy as np

import yasmin
from yasmin import State, Blackboard
from yasmin_ros.yasmin_node import YasminNode
from yasmin_ros.basic_outcomes import SUCCEED, ABORT

from nectar.control import (
    DroneFactory,
    MavrosDrone, 
    MavrosConfig,
    PoseSource,
    SITL_GAZEBO_CONFIG,
    )
from nectar.vision import ImageHandler
from nectar.vision.camera import ROSConfig
from nectar.control.types import RTLMethod

from walking_koala.constants import (
    SIM_IMAGE_SOURCE,
    SIM_IMAGE_COMPRESSED,
    INITIAL_TAKEOFF_ALTITUDE,
    RTL_ALTITUDE,
    BASE_LATITUDE,
    BASE_LONGITUDE,
)


class ReturnToLaunch(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT
        
        drone: MavrosDrone = blackboard["drone"]

        try:
            yasmin.YASMIN_LOG_INFO(f"Arming drone...")
            drone.arm()

            if not drone.is_armed:
                yasmin.YASMIN_LOG_ERROR("Drone is disarmed.")
                return ABORT

            yasmin.YASMIN_LOG_INFO(f"Returning to launch at {RTL_ALTITUDE}m...")
            drone.rtl(
                altitude=RTL_ALTITUDE,
                method=RTLMethod.NAVIGATE,
                land=True,
            )

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Return to launch failed: {e}.")
            return ABORT
