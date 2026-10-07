from app.smart_devices.smartthings_client import (
    SmartThingsClient
)


client = SmartThingsClient()


# ---------------------------------------------
# Test 1: Get devices
# ---------------------------------------------

devices = client.get_devices()

print("\n===== DEVICES =====")

for device in devices:

    print(
        device["name"],
        "→",
        device["deviceId"]
    )


# ---------------------------------------------
# Test 2: Find Samsung AC
# ---------------------------------------------

ac = None

for device in devices:

    if device["name"] == "Samsung Room A/C":

        ac = device
        break


if ac is None:

    print(
        "Samsung AC not found"
    )

    exit()


device_id = ac["deviceId"]


# ---------------------------------------------
# Test 3: Get AC status
# ---------------------------------------------

status = client.get_device_status(
    device_id
)


print("\n===== STATUS RECEIVED =====")

print(
    status
)