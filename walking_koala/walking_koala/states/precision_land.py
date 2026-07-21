import math
import time
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
    PIDController,
    )
from nectar.vision import ImageHandler
from nectar.vision.camera import ROSConfig

from walking_koala.constants import (
    SIM_IMAGE_SOURCE,
    SIM_IMAGE_COMPRESSED,
    INITIAL_TAKEOFF_ALTITUDE,
    BASE_LATITUDE,
    BASE_LONGITUDE,
    HOVER_COUNT,
    PRECISION_LAND_DURATION,
    P_XY,
    I_XY,
    D_XY,
    OUT_XY,
    INT_XY,
    P_Z,
    I_Z,
    D_Z,
    OUT_Z,
    INT_Z,
)

class PrecisionLand(State):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

        # Ver como usar a parte do PID
        # self.pid_x = PIDController(
        #     kp=P_XY
        #     ki=I_XY,
        #     kd=D_XY,
        #     output_limits=OUT_XY,
        #     integral_limits=INT_XY,
        # )

        # self.pid_y = PIDController(
        #     kp=P_XY
        #     ki=I_XY,
        #     kd=D_XY,
        #     output_limits=OUT_XY,
        #     integral_limits=INT_XY,
        # )

        # self.pid_z = PIDController(
        #     kp=P_Z,
        #     ki=I_Z,
        #     kd=D_Z,
        #     output_limits=OUT_Z,
        #     integral_limits=INT_Z,
        # )

    def execute(self, blackboard: Blackboard):
        if "drone" not in blackboard or not blackboard["drone"]:
            yasmin.YASMIN_LOG_ERROR("Drone not available.")
            return ABORT
        drone: MavrosDrone = blackboard["drone"]
        
        if "camera" not in blackboard or not blackboard["camera"]:
            yasmin.YASMIN_LOG_ERROR("Camera not available.")
        camera: ImageHandler = blackboard["camera"]

        try:
            yasmin.YASMIN_LOG_INFO("Moving to base with GPS...")
            if not self.move_to_base(drone):
                yasmin.YASMIN_LOG_ERROR("Drone failed to move to base.")
                return ABORT

            yasmin.YASMIN_LOG_INFO("Starting PID in landing base...")
            hover_count = 0;
            start = time.time()
            duration = PRECISION_LAND_DURATION

            while (time.time() - start < duration):
                if hover_count >= HOVER_COUNT:
                    yasmin.YASMIN_LOG_INFO("PID completed successfully.")
                    drone.move_velocity(0, 0, 0, 0)
                    return SUCCEED

                frame = camera.take_photo()
                cv2.imshow("frame", frame)
                cv2.waitKey()

                center = self.detect_landing_base(frame)

                if center is not None:
                    cx, cy = center
                    h, w = frame.shape

        except Exception as e:
            yasmin.YASMIN_LOG_ERROR(f"Precision landing failed: {e}")
            return ABORT


    def move_to_base(self, drone: MavrosDrone) -> bool:
        reached_base = drone.move_to_gps(BASE_LATITUDE, BASE_LONGITUDE)
        return reached_base


    def detect_landing_base(self, image) -> tuple:
        # Fazer o código de detectar o triângulo, retornando o centro
        pass

        