import os

from dotenv import load_dotenv
from typesafe_sdk import Choice, TypeSafeClient

from app.models.action import SaarthiAction


load_dotenv()


class JevService:

    def __init__(self):
        api_key = os.getenv("TYPESAFE_API_KEY")

        if not api_key:
            raise ValueError("TYPESAFE_API_KEY is missing")

        self.client = TypeSafeClient(api_key=api_key)

    def understand(self, text: str):

        response = self.client.system_one(
            state={
                "user_text": text
            },
            questions={

                "domain": Choice(

                    instructions=(
                        "Determine which part of Saarthi should handle "
                        "the user's request."
                    ),

                    criteria={

                        "BROWSER": (
                            "The user wants to control or interact "
                            "with a website or browser tab."
                        ),

                        "SMART_HOME": (
                            "The user wants to control a physical smart "
                            "home device such as an AC, fan, light, TV, "
                            "or other connected device."
                        ),

                        "OTHER": (
                            "The request does not belong to browser "
                            "or smart home control."
                        )
                    }
                ),

                "intent": Choice(

                    instructions=(
                        "Determine what the user wants Saarthi to do."
                    ),

                    criteria={

                        "OPEN": (
                            "The user wants to open or navigate "
                            "to a website."
                        ),

                        "SEARCH": (
                            "The user wants to search for something."
                        ),

                        "PLAY": (
                            "The user wants to play or start "
                            "music or video."
                        ),

                        "CLOSE": (
                            "The user wants to close the current "
                            "browser tab."
                        ),

                        "BACK": (
                            "The user wants to navigate back."
                        ),

                        "NEW_TAB": (
                            "The user wants to open a new browser tab."
                        ),

                        "READ": (
                            "The user wants Saarthi to read "
                            "or understand the current page."
                        ),

                        "REMIND": (
                            "The user wants to create a reminder."
                        ),

                        "TURN_ON": (
                            "The user wants to turn on a smart home device."
                        ),

                        "TURN_OFF": (
                            "The user wants to turn off a smart home device."
                        ),

                        "SET_TEMPERATURE": (
                            "The user wants to change the target temperature "
                            "of an AC or climate device."
                        ),

                        "SET_MODE": (
                            "The user wants to change the operating mode "
                            "of an AC or climate device."
                        ),

                        "SET_FAN_SPEED": (
                            "The user wants to change the fan speed "
                            "of an AC or climate device."
                        ),

                        "OTHER": (
                            "The request does not fit "
                            "the available actions."
                        ),
                    },
                ),

                "target": Choice(

                    instructions=(
                        "Determine which website, device, or other target "
                        "the user is referring to."
                    ),

                    criteria={

                        "YOUTUBE": (
                            "The user is referring to YouTube."
                        ),

                        "YOUTUBE_MUSIC": (
                            "The user is referring to YouTube Music."
                        ),

                        "SPOTIFY": (
                            "The user is referring to Spotify."
                        ),

                        "GOOGLE": (
                            "The user is referring to Google."
                        ),

                        "AMAZON": (
                            "The user is referring to Amazon."
                        ),

                        "GITHUB": (
                            "The user is referring to GitHub."
                        ),

                        "LEETCODE": (
                            "The user is referring to LeetCode."
                        ),

                        "GMAIL": (
                            "The user is referring to Gmail."
                        ),

                        "LINKEDIN": (
                            "The user is referring to LinkedIn."
                        ),

                        "CHATGPT": (
                            "The user is referring to ChatGPT."
                        ),

                        "GEMINI": (
                            "The user is referring to Gemini."
                        ),

                        "CURRENT_PAGE": (
                            "The user is referring to the currently "
                            "open browser page."
                        ),

                        "AC": (
                            "The user is referring to an air conditioner, "
                            "AC, air conditioning unit, or similar "
                            "climate device."
                        ),

                        "OTHER": (
                            "The user refers to another website, device, "
                            "or no specific target."
                        ),
                    },
                ),

                "value": Choice(

                    instructions=(
                        "Extract the main value associated with the user's "
                        "requested action. For temperature requests, "
                        "return the numeric temperature in degrees Celsius. "
                        "For AC mode requests, return the requested mode. "
                        "For fan speed requests, return the requested fan speed. "
                        "If the action does not require a value, return NONE."
                    ),

                    criteria={

                        "TEMPERATURE_16": (
                            "The requested AC temperature is 16 degrees Celsius."
                        ),

                        "TEMPERATURE_17": (
                            "The requested AC temperature is 17 degrees Celsius."
                        ),

                        "TEMPERATURE_18": (
                            "The requested AC temperature is 18 degrees Celsius."
                        ),

                        "TEMPERATURE_19": (
                            "The requested AC temperature is 19 degrees Celsius."
                        ),

                        "TEMPERATURE_20": (
                            "The requested AC temperature is 20 degrees Celsius."
                        ),

                        "TEMPERATURE_21": (
                            "The requested AC temperature is 21 degrees Celsius."
                        ),

                        "TEMPERATURE_22": (
                            "The requested AC temperature is 22 degrees Celsius."
                        ),

                        "TEMPERATURE_23": (
                            "The requested AC temperature is 23 degrees Celsius."
                        ),

                        "TEMPERATURE_24": (
                            "The requested AC temperature is 24 degrees Celsius."
                        ),

                        "TEMPERATURE_25": (
                            "The requested AC temperature is 25 degrees Celsius."
                        ),

                        "TEMPERATURE_26": (
                            "The requested AC temperature is 26 degrees Celsius."
                        ),

                        "TEMPERATURE_27": (
                            "The requested AC temperature is 27 degrees Celsius."
                        ),

                        "TEMPERATURE_28": (
                            "The requested AC temperature is 28 degrees Celsius."
                        ),

                        "TEMPERATURE_29": (
                            "The requested AC temperature is 29 degrees Celsius."
                        ),

                        "TEMPERATURE_30": (
                            "The requested AC temperature is 30 degrees Celsius."
                        ),

                        "COOL": (
                            "The requested AC mode is cool."
                        ),

                        "AUTO": (
                            "The requested AC mode is auto."
                        ),

                        "DRY": (
                            "The requested AC mode is dry."
                        ),

                        "FAN": (
                            "The requested AC mode is fan."
                        ),

                        "LOW": (
                            "The requested fan speed is low."
                        ),

                        "MEDIUM": (
                            "The requested fan speed is medium."
                        ),

                        "HIGH": (
                            "The requested fan speed is high."
                        ),

                        "TURBO": (
                            "The requested fan speed is turbo."
                        ),

                        "NONE": (
                            "The requested action does not require "
                            "an additional value."
                        ),
                    },
                ),
            },
        )

        domain_answer = response.choices["domain"]
        intent_answer = response.choices["intent"]
        target_answer = response.choices["target"]
        value_answer = response.choices["value"]

        value_choice = value_answer.choice

        if value_choice == "NONE":
            value = None

        elif value_choice.startswith("TEMPERATURE_"):
            value = int(
                value_choice.replace(
                    "TEMPERATURE_",
                    ""
                )
            )

        else:
            value = value_choice.lower()

        return SaarthiAction(
            domain=domain_answer.choice,
            action=intent_answer.choice,
            target=target_answer.choice,
            action_confidence=intent_answer.confidence,
            target_confidence=target_answer.confidence,
            value=value,
        )