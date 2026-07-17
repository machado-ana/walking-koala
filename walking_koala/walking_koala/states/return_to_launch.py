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
from nectar.control.types import RTLMethod, MoveReference

from walking_koala.constants import (
    SIM_IMAGE_SOURCE,
    SIM_IMAGE_COMPRESSED,
    INITIAL_TAKEOFF_ALTITUDE,
    RTL_ALTITUDE,
    BASE_LATITUDE,
    BASE_LONGITUDE,
    TAKEOFF_LATITUDE,
    TAKEOFF_LONGITUDE,
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
            yasmin.YASMIN_LOG_INFO(f"Drone taking off...")
            
            if not drone.takeoff(RTL_ALTITUDE):
                yasmin.YASMIN_LOG_ERROR("Can not return to launch. Drone takeoff failed.")
                return ABORT
            drone.delay(2)

            yasmin.YASMIN_LOG_INFO(f"Returning to launch at {RTL_ALTITUDE}m...")
            drone.move_to_gps(
                TAKEOFF_LATITUDE,
                TAKEOFF_LONGITUDE,
            )
            drone.delay(2)
            return SUCCEED

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Return to launch failed: {e}.")
            return ABORT
