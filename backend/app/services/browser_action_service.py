from app.models.action import SaarthiAction
from app.models.browser import BrowserCommand

from app.services.query_extractor import QueryExtractor
from urllib.parse import quote_plus

from app.services.play_query_extractor import PlayQueryExtractor


TARGET_URLS = {
    "YOUTUBE": "https://www.youtube.com",
    "YOUTUBE_MUSIC": "https://music.youtube.com",
    "SPOTIFY": "https://open.spotify.com",
    "GOOGLE": "https://www.google.com",
    "AMAZON": "https://www.amazon.in",
    "GITHUB": "https://github.com",
    "LEETCODE": "https://leetcode.com",
    "GMAIL": "https://mail.google.com",
    "LINKEDIN": "https://www.linkedin.com",
    "CHATGPT": "https://chatgpt.com",
}


    


class BrowserActionService:

    MIN_CONFIDENCE = 0.80

    def __init__(self):
        self.query_extractor = QueryExtractor()
        self.play_query_extractor = PlayQueryExtractor()

    def plan(
            self,
            action: SaarthiAction,
            original_text: str
            
            ) -> BrowserCommand | None:

        if action.action == "SEARCH":

            if action.action_confidence < self.MIN_CONFIDENCE:
                return None

            if action.target_confidence < self.MIN_CONFIDENCE:
                return None


            query = self.query_extractor.extract(
        original_text,
        action.target)

            print("\n===== QUERY EXTRACTION DEBUG =====")
            print("ORIGINAL TEXT:", original_text)
            print("TARGET:", action.target)
            print("EXTRACTED QUERY:", query)
            print("==================================\n")

            if not query:
                return None

            encoded_query = quote_plus(query)

            base_url = TARGET_URLS.get(
                action.target
            )

            if not base_url:
                return None

            if action.target == "YOUTUBE":

                url = (
                    "https://www.youtube.com/results"
                    f"?search_query={encoded_query}"
                )

                return BrowserCommand(
                    type="OPEN_URL",
                    url=url
                )

            if action.target == "LEETCODE":

                url = (
                    "https://leetcode.com/search"
                    f"?q={encoded_query}"
                )

                return BrowserCommand(
                    type="OPEN_URL",
                    url=url
                ) 

            if action.target == "GOOGLE":

                url = (
                    "https://www.google.com/search"
                    f"?q={encoded_query}"
                )

                return BrowserCommand(
                    type="OPEN_URL",
                    url=url
                )
            

            return None 

        if action.action == "PLAY":

            if action.action_confidence < self.MIN_CONFIDENCE:
                return None

            if action.target_confidence < self.MIN_CONFIDENCE:
                return None

            if action.target != "YOUTUBE":
                return None

            query = self.play_query_extractor.extract(
                original_text
            )

            print("\n===== PLAY QUERY DEBUG =====")
            print("ORIGINAL TEXT:", original_text)
            print("EXTRACTED PLAY QUERY:", query)
            print("============================\n")

            if not query:
                return None

            return BrowserCommand(
                type="PLAY_YOUTUBE",
                query=query
            )
              

        if action.action == "OPEN":

            if action.action_confidence < self.MIN_CONFIDENCE:
                return None

            if action.target_confidence < self.MIN_CONFIDENCE:
                return None

            url = TARGET_URLS.get(action.target)

            if not url:
                return None

            return BrowserCommand(
                type="OPEN_URL",
                url=url
            )

        if action.action == "BACK":

            if action.action_confidence < self.MIN_CONFIDENCE:
                return None

            return BrowserCommand(
                type="GO_BACK"
            )

        if action.action == "NEW_TAB":

            if action.action_confidence < self.MIN_CONFIDENCE:
                return None

            return BrowserCommand(
                type="NEW_TAB"
            )

        if action.action == "CLOSE":

            if action.action_confidence < 0.95:
                return None

            return BrowserCommand(
                type="CLOSE_TAB"
            )

        return None