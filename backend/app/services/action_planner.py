import re

from app.models.action import SaarthiAction
from app.models.action_plan import ActionPlan


class ActionPlanner:

    TEMPERATURE_PATTERN = re.compile(
        r"\b(?P<temperature>\d{2})\s*"
        r"(?:degree|degrees|°c|c)?\s*"
        r"(?:pe|par|me|mein|set|kar)"
    )

    MODE_PATTERN = re.compile(
        r"\b(?P<mode>cool|auto|dry|fan)\s+mode\b"
    )

    FAN_PATTERN = re.compile(
        r"\b(?:fan\s+)"
        r"(?P<speed>low|medium|high|turbo)\b"
    )

    TURN_ON_PATTERNS = (
        "chala do",
        "chala de",
        "on kar do",
        "on kr do",
        "turn on",
        "switch on",
        "start kar do",
        "start kr do",
    )

    TURN_OFF_PATTERNS = (
        "band kar do",
        "band kr do",
        "turn off",
        "switch off",
        "off kar do",
        "off kr do",
        "bujha do",
    )

    def build_plan(
        self,
        primary_action: SaarthiAction,
        original_text: str
    ) -> ActionPlan:

        text = original_text.lower()

        if primary_action.domain != "SMART_HOME":
            return ActionPlan(
                actions=[primary_action]
            )

        if primary_action.target != "AC":
            return ActionPlan(
                actions=[primary_action]
            )

        actions = []

        # -------------------------------------------------
        # 1. POWER ACTION
        # -------------------------------------------------

        if self._contains_any(
            text,
            self.TURN_ON_PATTERNS
        ):
            actions.append(
                self._create_action(
                    primary_action,
                    action="TURN_ON"
                )
            )

        elif self._contains_any(
            text,
            self.TURN_OFF_PATTERNS
        ):
            actions.append(
                self._create_action(
                    primary_action,
                    action="TURN_OFF"
                )
            )

        # -------------------------------------------------
        # 2. TEMPERATURE
        # -------------------------------------------------

        temperature = self._extract_temperature(text)

        if temperature is not None:
            actions.append(
                self._create_action(
                    primary_action,
                    action="SET_TEMPERATURE",
                    value=temperature
                )
            )

        # -------------------------------------------------
        # 3. MODE
        # -------------------------------------------------

        mode = self._extract_mode(text)

        if mode is not None:
            actions.append(
                self._create_action(
                    primary_action,
                    action="SET_MODE",
                    value=mode
                )
            )

        # -------------------------------------------------
        # 4. FAN SPEED
        # -------------------------------------------------

        fan_speed = self._extract_fan_speed(text)

        if fan_speed is not None:
            actions.append(
                self._create_action(
                    primary_action,
                    action="SET_FAN_SPEED",
                    value=fan_speed
                )
            )

        # -------------------------------------------------
        # 5. FALLBACK
        # -------------------------------------------------

        if not actions:
            actions.append(primary_action)

        return ActionPlan(
            actions=actions
        )

    def _create_action(
        self,
        primary_action: SaarthiAction,
        action: str,
        value=None
    ) -> SaarthiAction:

        return SaarthiAction(
            domain="SMART_HOME",
            action=action,
            target=primary_action.target,
            action_confidence=primary_action.action_confidence,
            target_confidence=primary_action.target_confidence,
            value=value
        )

    def _contains_any(
        self,
        text: str,
        patterns: tuple[str, ...]
    ) -> bool:

        return any(
            pattern in text
            for pattern in patterns
        )

    def _extract_temperature(
        self,
        text: str
    ) -> int | None:

        match = self.TEMPERATURE_PATTERN.search(text)

        if not match:
            return None

        temperature = int(
            match.group("temperature")
        )

        if not 16 <= temperature <= 30:
            return None

        return temperature

    def _extract_mode(
        self,
        text: str
    ) -> str | None:

        match = self.MODE_PATTERN.search(text)

        if not match:
            return None

        return match.group("mode")

    def _extract_fan_speed(
        self,
        text: str
    ) -> str | None:

        match = self.FAN_PATTERN.search(text)

        if not match:
            return None

        return match.group("speed")