from app.smart_devices.smartthings_client import SmartThingsClient
from app.smart_devices.ac_controller import ACController
from app.smart_devices.smart_home_executor import SmartHomeExecutor


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


print("\n===== TURN ON =====")
print(
    executor.execute("TURN_ON")
)


print("\n===== TEMPERATURE =====")
print(
    executor.execute(
        "SET_TEMPERATURE",
        29
    )
)


print("\n===== MODE =====")
print(
    executor.execute(
        "SET_MODE",
        "cool"
    )
)


print("\n===== FAN =====")
print(
    executor.execute(
        "SET_FAN_SPEED",
        "high"
    )
)


print("\n===== FINAL STATUS =====")

status = ac.get_status()

print("Power       :", status.power)
print("Mode        :", status.mode)
print("Target Temp :", status.target_temperature)
print("Room Temp   :", status.room_temperature)
print("Fan Speed   :", status.fan_speed)