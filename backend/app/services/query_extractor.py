import re


class QueryExtractor:

    SEARCH_PATTERN = re.compile(
        r"^(?P<target>.+?)\s+"
        r"(?:pe|par|per)\s+"
        r"(?P<query>.+?)"
        r"(?:\s+(?:ko|ka|ki|ke))?"
        r"\s+search(?:\s+(?:karo|kar|kro))?\s*$",
        re.IGNORECASE
    )

    def extract(
        self,
        text: str,
        target: str
    ) -> str | None:

        if not text:
            return None

        text = text.strip()

        if not text:
            return None

        match = self.SEARCH_PATTERN.match(text)

        if not match:
            return None

        query = match.group("query").strip()

        if not query:
            return None

        return query