from app.smart_devices.smartthings_client import SmartThingsClient
from app.smart_devices.ac_status import ACStatus


class ACController:

    MIN_TEMPERATURE = 16
    MAX_TEMPERATURE = 30

    SUPPORTED_MODES = {
        "auto",
        "cool",
        "dry",
        "fan"
    }

    SUPPORTED_FAN_SPEEDS = {
        "auto",
        "low",
        "medium",
        "high",
        "turbo"
    }

    def __init__(
        self,
        client: SmartThingsClient,
        device_id: str
    ):

        self.client = client
        self.device_id = device_id

    # --------------------------------------------------
    # Internal helpers
    # --------------------------------------------------

    def _send_command(self, command: dict):

        return self.client.send_command(
            self.device_id,
            command
        )

    def _set_power(self, state: str):

        command = {
            "commands": [
                {
                    "component": "main",
                    "capability": "switch",
                    "command": state,
                    "arguments": []
                }
            ]
        }

        return self._send_command(command)

    # --------------------------------------------------
    # Public AC operations
    # --------------------------------------------------

    def turn_on(self):

        return self._set_power("on")

    def turn_off(self):

        return self._set_power("off")

    def set_temperature(
        self,
        temperature: int
    ):

        if not (
            self.MIN_TEMPERATURE
            <= temperature
            <= self.MAX_TEMPERATURE
        ):
            raise ValueError(
                f"Temperature must be between "
                f"{self.MIN_TEMPERATURE} and "
                f"{self.MAX_TEMPERATURE}."
            )

        command = {
            "commands": [
                {
                    "component": "main",
                    "capability":
                        "thermostatCoolingSetpoint",
                    "command":
                        "setCoolingSetpoint",
                    "arguments": [
                        temperature
                    ]
                }
            ]
        }

        return self._send_command(command)

    def set_mode(
        self,
        mode: str
    ):

        mode = mode.lower()

        if mode not in self.SUPPORTED_MODES:
            raise ValueError(
                f"Unsupported AC mode: {mode}"
            )

        command = {
            "commands": [
                {
                    "component": "main",
                    "capability":
                        "airConditionerMode",
                    "command":
                        "setAirConditionerMode",
                    "arguments": [
                        mode
                    ]
                }
            ]
        }

        return self._send_command(command)

    def set_fan_speed(
        self,
        speed: str
    ):

        speed = speed.lower()

        if speed not in self.SUPPORTED_FAN_SPEEDS:
            raise ValueError(
                f"Unsupported fan speed: {speed}"
            )

        command = {
            "commands": [
                {
                    "component": "main",
                    "capability":
                        "airConditionerFanMode",
                    "command":
                        "setFanMode",
                    "arguments": [
                        speed
                    ]
                }
            ]
        }

        return self._send_command(command)

    def get_status(self) -> ACStatus:

        status = self.client.get_device_status(
            self.device_id
        )

        main = status["components"]["main"]

        return ACStatus(
            power=main["switch"]["switch"]["value"],
            mode=main[
                "airConditionerMode"
            ][
                "airConditionerMode"
            ]["value"],
            target_temperature=main[
                "thermostatCoolingSetpoint"
            ][
                "coolingSetpoint"
            ]["value"],
            room_temperature=main[
                "temperatureMeasurement"
            ][
                "temperature"
            ]["value"],
            fan_speed=main[
                "airConditionerFanMode"
            ][
                "fanMode"
            ]["value"]
        )