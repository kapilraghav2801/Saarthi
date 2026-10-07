import time

from app.models.action_plan import ActionPlan
from app.smart_devices.ac_controller import ACController
from app.smart_devices.execution_result import ExecutionResult


class SmartHomeExecutor:

    def __init__(self, ac_controller: ACController):
        self.ac = ac_controller

    def _wait_for_power_state(
        self,
        expected_state: str,
        timeout: int = 10,
        interval: int = 1
    ) -> bool:

        elapsed = 0

        while elapsed < timeout:

            status = self.ac.get_status()

            if status.power == expected_state:
                return True

            time.sleep(interval)
            elapsed += interval

        return False

    def _wait_for_temperature(
        self,
        expected_temperature: int,
        timeout: int = 10,
        interval: int = 1
    ) -> bool:

        elapsed = 0

        while elapsed < timeout:

            status = self.ac.get_status()

            if status.target_temperature == expected_temperature:
                return True

            time.sleep(interval)
            elapsed += interval

        return False

    def _wait_for_mode(
        self,
        expected_mode: str,
        timeout: int = 10,
        interval: int = 1
    ) -> bool:

        elapsed = 0

        while elapsed < timeout:

            status = self.ac.get_status()

            if status.mode == expected_mode:
                return True

            time.sleep(interval)
            elapsed += interval

        return False

    def _wait_for_fan_speed(
        self,
        expected_speed: str,
        timeout: int = 10,
        interval: int = 1
    ) -> bool:

        elapsed = 0

        while elapsed < timeout:

            status = self.ac.get_status()

            if status.fan_speed == expected_speed:
                return True

            time.sleep(interval)
            elapsed += interval

        return False

    def execute(
        self,
        action: str,
        value=None
    ) -> ExecutionResult:

        if action == "TURN_ON":

            self.ac.turn_on()

            verified = self._wait_for_power_state("on")

            if not verified:
                return ExecutionResult(
                    success=False,
                    message=(
                        "AC did not turn on "
                        "within the expected time."
                    ),
                    reason="POWER_STATE_TIMEOUT"
                )

            return ExecutionResult(
                success=True,
                message="AC turned on."
            )

        if action == "TURN_OFF":

            self.ac.turn_off()

            verified = self._wait_for_power_state("off")

            if not verified:
                return ExecutionResult(
                    success=False,
                    message=(
                        "AC did not turn off "
                        "within the expected time."
                    ),
                    reason="POWER_STATE_TIMEOUT"
                )

            return ExecutionResult(
                success=True,
                message="AC turned off."
            )

        if action == "SET_TEMPERATURE":

            status = self.ac.get_status()

            if status.power == "off":
                return ExecutionResult(
                    success=False,
                    message="AC is currently off.",
                    reason="DEVICE_OFF"
                )

            self.ac.set_temperature(value)

            verified = self._wait_for_temperature(value)

            if not verified:
                return ExecutionResult(
                    success=False,
                    message=(
                        f"AC did not confirm "
                        f"{value}°C within the expected time."
                    ),
                    reason="TEMPERATURE_UPDATE_TIMEOUT"
                )

            return ExecutionResult(
                success=True,
                message=f"AC temperature set to {value}°C."
            )

        if action == "SET_MODE":

            status = self.ac.get_status()

            if status.power == "off":
                return ExecutionResult(
                    success=False,
                    message="AC is currently off.",
                    reason="DEVICE_OFF"
                )

            self.ac.set_mode(value)

            verified = self._wait_for_mode(value.lower())

            if not verified:
                return ExecutionResult(
                    success=False,
                    message=(
                        f"AC did not confirm "
                        f"{value} mode within "
                        f"the expected time."
                    ),
                    reason="MODE_UPDATE_TIMEOUT"
                )

            return ExecutionResult(
                success=True,
                message=f"AC mode set to {value}."
            )

        if action == "SET_FAN_SPEED":

            status = self.ac.get_status()

            if status.power == "off":
                return ExecutionResult(
                    success=False,
                    message="AC is currently off.",
                    reason="DEVICE_OFF"
                )

            self.ac.set_fan_speed(value)

            verified = self._wait_for_fan_speed(
                value.lower()
            )

            if not verified:
                return ExecutionResult(
                    success=False,
                    message=(
                        f"AC did not confirm "
                        f"fan speed {value} within "
                        f"the expected time."
                    ),
                    reason="FAN_SPEED_UPDATE_TIMEOUT"
                )

            return ExecutionResult(
                success=True,
                message=f"AC fan speed set to {value}."
            )

        raise ValueError(
            f"Unsupported smart home action: {action}"
        )

    def execute_plan(
        self,
        plan: ActionPlan
    ) -> list[dict]:

        results = []

        for planned_action in plan.actions:

            print(
                f"Executing: "
                f"{planned_action.action} "
                f"→ {planned_action.value}"
            )

            result = self.execute(
                action=planned_action.action,
                value=planned_action.value
            )

            results.append(
                {
                    "action": planned_action.model_dump(),
                    "result": result.model_dump()
                }
            )

            if not result.success:
                break

        return results