import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict

from app.services.jev_service import JevService
from app.services.browser_action_service import BrowserActionService
from app.services.action_planner import ActionPlanner
from app.services.plan_validator import PlanValidator

from app.smart_devices.smartthings_client import SmartThingsClient
from app.smart_devices.ac_controller import ACController
from app.smart_devices.smart_home_executor import SmartHomeExecutor


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


jev_service = JevService()
browser_action_service = BrowserActionService()
action_planner = ActionPlanner()
plan_validator = PlanValidator()


smartthings_client = SmartThingsClient()

ac_device_id = os.getenv("SMARTTHINGS_AC_DEVICE_ID")

if not ac_device_id:
    raise ValueError("SMARTTHINGS_AC_DEVICE_ID is missing")


ac_controller = ACController(
    smartthings_client,
    ac_device_id
)

smart_home_executor = SmartHomeExecutor(
    ac_controller
)


class BrowserAnalysisRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str


@app.post("/browser/analyze")
async def browser_analyze(
    request: BrowserAnalysisRequest
):

    action = jev_service.understand(
        request.text
    )

    print("\n==============================")
    print("USER TEXT:", request.text)
    print("DOMAIN:", action.domain)
    print("ACTION:", action.action)
    print("TARGET:", action.target)
    print("VALUE:", action.value)
    print(
        "ACTION CONFIDENCE:",
        action.action_confidence
    )
    print(
        "TARGET CONFIDENCE:",
        action.target_confidence
    )
    print("==============================\n")

    if action.domain == "SMART_HOME":

        if action.target != "AC":

            return {
                "success": False,
                "domain": "SMART_HOME",
                "action": action.model_dump(),
                "result": {
                    "success": False,
                    "message": (
                        "This smart device "
                        "is not supported yet."
                    ),
                    "reason": "UNSUPPORTED_DEVICE"
                }
            }

        # -----------------------------------------
        # Step 1: Build raw action plan
        # -----------------------------------------

        plan = action_planner.build_plan(
            action,
            request.text
        )

        print("\n===== RAW ACTION PLAN =====")

        for index, planned_action in enumerate(
            plan.actions,
            start=1
        ):
            print(
                f"{index}. "
                f"{planned_action.action} "
                f"→ {planned_action.value}"
            )

        print("===========================\n")

        # -----------------------------------------
        # Step 2: Validate and order the plan
        # -----------------------------------------

        (
            is_valid,
            validation_error,
            plan
        ) = plan_validator.validate_and_order(
            plan
        )

        if not is_valid:

            print(
                "PLAN REJECTED:",
                validation_error
            )

            return {
                "success": False,
                "domain": "SMART_HOME",
                "action": action.model_dump(),
                "plan": plan.model_dump(),
                "message": validation_error,
                "reason": "INVALID_ACTION_PLAN"
            }

        print("\n===== VALIDATED ACTION PLAN =====")

        for index, planned_action in enumerate(
            plan.actions,
            start=1
        ):
            print(
                f"{index}. "
                f"{planned_action.action} "
                f"→ {planned_action.value}"
            )

        print("=================================\n")

        # -----------------------------------------
        # Step 3: Execute the validated plan
        # -----------------------------------------

        results = smart_home_executor.execute_plan(
            plan
        )

        success = all(
            item["result"]["success"]
            for item in results
        )

        return {
            "success": success,
            "domain": "SMART_HOME",
            "action": action.model_dump(),
            "plan": plan.model_dump(),
            "results": results
        }

    if action.domain == "BROWSER":

        command = browser_action_service.plan(
            action,
            request.text
        )

        return {
            "success": command is not None,
            "domain": "BROWSER",
            "action": action.model_dump(),
            "command": (
                command.model_dump()
                if command
                else None
            )
        }

    return {
        "success": False,
        "domain": action.domain,
        "action": action.model_dump(),
        "message": (
            "I cannot handle "
            "this request yet."
        )
    }