from app.smart_devices.smartthings_client import SmartThingsClient
from app.smart_devices.ac_controller import ACController


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
ac.turn_off()


status = ac.get_status()

print("\n===== CLEAN AC STATUS =====")

print("Power       :", status.power)
print("Mode        :", status.mode)
print("Target Temp :", status.target_temperature)
print("Room Temp   :", status.room_temperature)
print("Fan Speed   :", status.fan_speed)