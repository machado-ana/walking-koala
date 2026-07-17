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

from walking_koala.constants import (
    SIM_IMAGE_SOURCE,
    SIM_IMAGE_COMPRESSED,
    INITIAL_TAKEOFF_ALTITUDE,
    BASE_LATITUDE,
    BASE_LONGITUDE,
)

class PrecisionLand(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

    def execute(self, blackboard: Blackboard):
        drone: MavrosDrone = blackboard["drone"]
        camera: ImageHandler = blackboard["camera"]

        try:
            if not self.move_to_base(drone):
                return ABORT
            return SUCCEED

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Moving to base failed: {e}")
            return ABORT

    def move_to_base(self, drone: MavrosDrone) -> bool:
        yasmin.YASMIN_LOG_INFO("Moving to base...")

        drone.move_to_gps(
            BASE_LATITUDE,
            BASE_LONGITUDE,
            )
        drone.delay(1)
        return True
        