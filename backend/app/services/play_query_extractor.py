import re


class PlayQueryExtractor:

    PLAY_PATTERN = re.compile(
        r"^(?P<target>.+?)\s+"
        r"(?:pe|par|per)\s+"
        r"(?P<query>.+?)"
        r"\s+"
        r"(?:"
        r"chalao"
        r"|chala(?:\s+(?:do|de|dena))?"
        r"|play"
        r"|bajao"
        r"|baja(?:\s+(?:do|de|dena))?"
        r"|lagao"
        r"|laga(?:\s+(?:do|de|dena))?"
        r")"
        r"\s*$",
        re.IGNORECASE
    )

    def extract(
        self,
        text: str
    ) -> str | None:

        if not text:
            return None

        text = text.strip()

        if not text:
            return None

        match = self.PLAY_PATTERN.match(text)

        if not match:
            return None

        query = match.group("query").strip()

        if not query:
            return None

        return query