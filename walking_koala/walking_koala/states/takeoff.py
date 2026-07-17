import cv2
import numpy as np

import yasmin
from yasmin import State, Blackboard
from yasmin_ros.yasmin_node import YasminNode
from yasmin_ros.basic_outcomes import SUCEED, ABORT

from nectar.control import (
    DroneFactory,
    MavrosDrone, 
    MavrosConfig,
    PoseSource,
    SITL_GAZEBO_CONFIG,
    )
from nectar.vision import ImageHandler
from nectar.vision.camera import ROSConfig

from walking_koala.constants import (
    SIM_IMAGE_SOURCE,
    SIM_IMAGE_COMPRESSED,
    INITIAL_TAKEOFF_ALTITUDE,
)


class Takeoff(State):
    def __init__(self):
        super().__init__(outcomes=[SUCEED, ABORT])
    
    def execute(self, blackboard : Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT
        
        drone: MavrosDrone = blackboard["drone"]

        try:
            yasmin.YASMIN_LOG_INFO(f"Taking of to {INITIAL_TAKEOFF_ALTITUDE}m...")

            reached = drone.takeoff(INITIAL_TAKEOFF_ALTITUDE)
            drone.delay(2)

            if not reached:
                yasmin.YASMIN_LOG_WARN("Takeoff move_to timed out, continuing.")

            drone.delay(1)
            yasmin.YASMIN_LOG_INFO("Takeoff complete.")
            return SUCEED
        
        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Takeoff failed: {e}")
            return ABORT
