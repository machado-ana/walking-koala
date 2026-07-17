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
)


class Initialize(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

    def execute(self, blackboard: Blackboard):
        try:
            node = YasminNode.get_instance()

            yasmin.YASMIN_LOG_INFO("Initializing drone...")
            config = SITL_GAZEBO_CONFIG
            drone = DroneFactory.create("mavros", config, node)
            blackboard["drone"] = drone

        # Don't know if camera will be initialized here
        # yasmin.YASMIN_LOG_INFO("Initializing camera...")
        # cam_config = ROSConfig(
        #     topic=SIM_IMAGE_SOURCE, 
        #     compressed=SIM_IMAGE_COMPRESSED,
        #     )
        # camera = ImageHandler (
        #     node=node,
        #     image_source=SIM_IMAGE_SOURCE,
        #     config=cam_config
        # )
        # camera.open()
        # frame = camera.take_photo()
        # if frame is None:
        #     yasmin.YASMIN_LOG_ERROR("Failed to get frame from camera.")
        #     return ABORT
        # yasmin.YASMIN_LOG_INFO(
        #     f"Camera ready. Frame Shape: {frame.shape}"
        #     )
        # blackboard["camera"] = camera

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Initialization failed: {e}")
            return ABORT
