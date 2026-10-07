import os

import requests
from dotenv import load_dotenv


class SmartThingsClient:

    BASE_URL = "https://api.smartthings.com/v1"

    def __init__(self):

        load_dotenv()

        self.token = os.getenv(
            "SMARTTHINGS_TOKEN"
        )

        if not self.token:
            raise ValueError(
                "SMARTTHINGS_TOKEN is missing"
            )

        self.headers = {
            "Authorization":
                f"Bearer {self.token}",

            "Content-Type":
                "application/json",

            "Accept":
                "application/json",
        }

    def get_devices(self):

        response = requests.get(
            f"{self.BASE_URL}/devices",
            headers=self.headers,
        )

        response.raise_for_status()

        return response.json()["items"]

    def get_device_status(
        self,
        device_id: str
    ):

        response = requests.get(
            f"{self.BASE_URL}/devices/{device_id}/status",
            headers=self.headers,
        )

        response.raise_for_status()

        return response.json()

    def send_command(
        self,
        device_id: str,
        command: dict
    ):

        response = requests.post(
            f"{self.BASE_URL}/devices/{device_id}/commands",
            headers=self.headers,
            json=command,
        )

        response.raise_for_status()

        return response.json()