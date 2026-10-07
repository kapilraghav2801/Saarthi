from app.services.jev_service import JevService


jev = JevService()


commands = [
    "YouTube kholo",
    "Amazon kholo",
    "Google khol",
    "YouTube pe Honey Singh search karo",
    "Google pe Python FastAPI search kar",
    "YouTube pe Honey Singh ka song chala",
    "Honey Singh ka koi song chala do",
    "web pe FastAPI ke docs dhundho",
    "Amazon pe iPhone search karo",
    "YouTube pe isko search karo",
    "isko play karo",
    "isko search karo",
]


for command in commands:

    result = jev.understand(command)

    print("\n" + "=" * 70)
    print("USER              :", command)
    print("ACTION            :", result.action)
    print("ACTION CONFIDENCE :", result.action_confidence)
    print("TARGET            :", result.target)
    print("TARGET CONFIDENCE :", result.target_confidence)