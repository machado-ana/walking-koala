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
    RTL_ALTITUDE,
    BASE_LATITUDE,
    BASE_LONGITUDE,
)


class ReturnToLaunch(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

    def execute(self, blackboard: Blackboard):
        pass
