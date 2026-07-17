import rclpy

import yasmin
from yasmin import StateMachine
from yasmin_ros import set_ros_loggers
from yasmin_ros.basic_outcomes import SUCCEED, FAIL, TIMEOUT, ABORT

from walking_koala.states import(
    Initialize,
    Takeoff,
    PrecisionLand,
    Land,
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
            transitions={SUCCEED:"LAND", ABORT:"LAND"}
        )
        self.add_state(
            "PRECISION_LAND",
            PrecisionLand(),
            transitions={SUCCEED:"LAND", ABORT:"LAND"}
        )
        self.add_state(
            "LAND",
            Land(),
            transitions={SUCCEED:SUCCEED, ABORT:ABORT}
        )

        self.set_start_state("INITIALIZE")

def main():
    rclpy.init()

    set_ros_loggers()

    mission_sm = Mission()

    try:
        final_outcome = mission_sm
        yasmin.YASMIN_LOG_INFO(final_outcome)
    except KeyboardInterrupt:
        if mission_sm.is_running():
            mission_sm.cancel_state()

    if rclpy.ok():
        rclpy.shutdown()

if __name__ == "__main__":
    main()