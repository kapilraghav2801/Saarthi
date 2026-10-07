from app.smart_devices.smartthings_client import SmartThingsClient
from app.smart_devices.ac_controller import ACController
from app.smart_devices.smart_home_executor import SmartHomeExecutor

import time


client = SmartThingsClient()

devices = client.get_devices()

device_id = None

for device in devices:

    if device["name"] == "Samsung Room A/C":

        device_id = device["deviceId"]
        break


if device_id is None:

    print("Samsung AC not found")
    exit()


ac = ACController(
    client,
    device_id
)

executor = SmartHomeExecutor(ac)


print("\n===== TURN ON AC =====")

executor.execute(
    "TURN_ON"
)

#time.sleep(3)

print("\n===== TRY SET TEMPERATURE =====")

result = executor.execute(
    "SET_TEMPERATURE",
    29
)

print(result)

#time.sleep(3)

print("\n===== CURRENT STATUS =====")

status = ac.get_status()

print("Power       :", status.power)
print("Mode        :", status.mode)
print("Target Temp :", status.target_temperature)
print("Room Temp   :", status.room_temperature)
print("Fan Speed   :", status.fan_speed)

print("DEVICE ID : ", device_id)