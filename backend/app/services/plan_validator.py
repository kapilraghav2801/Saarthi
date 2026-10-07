from app.models.action_plan import ActionPlan


class PlanValidator:

    ACTION_PRIORITY = {
        "TURN_ON": 1,
        "SET_MODE": 2,
        "SET_TEMPERATURE": 3,
        "SET_FAN_SPEED": 4,
        "TURN_OFF": 5,
    }

    def validate(
        self,
        plan: ActionPlan
    ) -> tuple[bool, str | None]:

        actions = plan.actions

        if not actions:
            return False, "Action plan is empty."

        action_names = [
            action.action
            for action in actions
        ]

        # ---------------------------------------------
        # Rule 1: TURN_ON and TURN_OFF together
        # ---------------------------------------------

        if (
            "TURN_ON" in action_names
            and "TURN_OFF" in action_names
        ):
            return (
                False,
                "TURN_ON and TURN_OFF cannot be "
                "requested in the same action plan."
            )

        # ---------------------------------------------
        # Rule 2: TURN_OFF + device settings
        # ---------------------------------------------

        if "TURN_OFF" in action_names:

            setting_actions = {
                "SET_TEMPERATURE",
                "SET_MODE",
                "SET_FAN_SPEED",
            }

            has_setting = any(
                action in setting_actions
                for action in action_names
            )

            if has_setting:
                return (
                    False,
                    "Cannot change AC settings "
                    "while also turning the AC off."
                )

        # ---------------------------------------------
        # Rule 3: SET_TEMPERATURE requires a value
        # ---------------------------------------------

        for action in actions:

            if action.action == "SET_TEMPERATURE":

                if action.value is None:
                    return (
                        False,
                        "SET_TEMPERATURE requires "
                        "a temperature value."
                    )

        # ---------------------------------------------
        # Rule 4: SET_MODE requires a value
        # ---------------------------------------------

        for action in actions:

            if action.action == "SET_MODE":

                if action.value is None:
                    return (
                        False,
                        "SET_MODE requires "
                        "a mode value."
                    )

        # ---------------------------------------------
        # Rule 5: SET_FAN_SPEED requires a value
        # ---------------------------------------------

        for action in actions:

            if action.action == "SET_FAN_SPEED":

                if action.value is None:
                    return (
                        False,
                        "SET_FAN_SPEED requires "
                        "a fan speed value."
                    )

        return True, None

    def order(
        self,
        plan: ActionPlan
    ) -> ActionPlan:

        ordered_actions = sorted(
            plan.actions,
            key=lambda action: self.ACTION_PRIORITY.get(
                action.action,
                999
            )
        )

        return ActionPlan(
            actions=ordered_actions
        )

    def validate_and_order(
        self,
        plan: ActionPlan
    ) -> tuple[bool, str | None, ActionPlan]:

        is_valid, error = self.validate(plan)

        if not is_valid:
            return (
                False,
                error,
                plan
            )

        ordered_plan = self.order(plan)

        return (
            True,
            None,
            ordered_plan
        )