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


class Land(State):
    def __init__(self):
        super().__init__(outcomes=[SUCEED, ABORT])
    
    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT
        
        drone: MavrosDrone = blackboard["drone"]

        try: 
            drone.land()
            drone.delay(10)
            yasmin.YASMIN_LOG_INFO("Landed.")

            if "camera" in blackboard and blackboard["camera"]:
                blackboard["camera"].cleanup()
            
            return SUCEED
        
        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Landing failed: {e}")
            return ABORT
        
