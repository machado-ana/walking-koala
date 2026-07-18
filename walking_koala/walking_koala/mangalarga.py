import rclpy

import yasmin
from yasmin import StateMachine
from yasmin_ros import set_ros_loggers
from yasmin_ros.yasmin_node import YasminNode
from yasmin_ros.basic_outcomes import SUCCEED, FAIL, TIMEOUT, ABORT

import nectar

from walking_koala.states import(
    Initialize,
    Takeoff,
    PrecisionLand,
    Land,
    ReturnToLaunch,
)

class Mission(StateMachine):
    def __init__(self):
        super().__init__(outcomes=[SUCCEED, ABORT])

        self.add_state(
            "INITIALIZE",
            Initialize(),
            transitions={SUCCEED:"TAKEOFF", ABORT:ABORT}
        )

        self.add_state(
            "TAKEOFF",
            Takeoff(),
            transitions={SUCCEED:"PRECISION_LAND", ABORT:"LAND"}
        )

        self.add_state(
            "PRECISION_LAND",
            PrecisionLand(),
            transitions={SUCCEED:"LAND", ABORT:"LAND"}
        )

        self.add_state(
            "LAND",
            Land(),
            transitions={SUCCEED:"RTL", ABORT:ABORT}
        )

        self.add_state(
            "RTL",
            ReturnToLaunch(),
            transitions={SUCCEED:SUCCEED, ABORT:ABORT}
        )

        self.set_start_state("INITIALIZE")

def main():
    rclpy.init()

    nectar.use_executor(YasminNode.get_instance()._executor)

    set_ros_loggers()

    mission_sm = Mission()

    try:
        final_outcome = mission_sm()
        yasmin.YASMIN_LOG_INFO(final_outcome)
    except KeyboardInterrupt:
        if mission_sm.is_running():
            mission_sm.cancel_state()

    if rclpy.ok():
        rclpy.shutdown()

if __name__ == "__main__":
    main()
