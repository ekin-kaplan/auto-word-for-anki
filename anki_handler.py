import json
import requests

class AnkiHandler:
    def __init__(self, url="http://127.0.0.1:8765"):
        self.url = url
        self.deck_name = "Business English"
        # 1. Advanced Headers
        self.headers = {
            "Content-Type": "application/json",
            "User-Agent": "Anki-AI-Automator"
        }

    def _invoke(self, action, **params):
        # 2. Correct Payload Construction (Fixing potential syntax error in json.dumps)
        payload = {
            "action": action,
            "version": 6,
            "params": params
        }
        
        # 3. JSON Serialization
        requestJson = json.dumps(payload)

        try:
            # 4. Explicit Headers and Data
            response = requests.post(self.url, data=requestJson, headers=self.headers, timeout=5).json()
            
            if len(response) != 2:
                raise Exception("Response has an unexpected number of fields.")
            if "error" not in response:
                raise Exception("Response is missing required error field.")
            if "result" not in response:
                raise Exception("Response is missing required result field.")
            if response["error"] is not None:
                raise Exception(response["error"])
            return response["result"]
            
        except Exception as e:
            # 5. Detailed Debug Logging
            print(f"DEBUG: Anki Connection Technical Error: {e}")
            
            # Re-raise friendly errors for the UI
            if isinstance(e, requests.exceptions.ConnectionError):
                raise Exception("Anki bağlantısı sağlanamadı. Lütfen Anki'nin açık olduğundan emin olun.")
            elif isinstance(e, requests.exceptions.Timeout):
                raise Exception("Anki bağlantısı zaman aşımına uğradı.")
            else:
                raise e

    def check_connection(self):
        """Checks if AnkiConnect is reachable."""
        try:
            self._invoke("version")
            return True
        except Exception:
            return False

    def create_deck_if_not_exists(self):
        """Creates the 'Business English' deck if it doesn't exist."""
        try:
            decks = self._invoke("deckNames")
            if self.deck_name not in decks:
                self._invoke("createDeck", deck=self.deck_name)
                return True # Created
            return False # Already exists
        except Exception as e:
            print(f"Error creating deck: {e}")
            return False

    def add_card(self, word, preview_tr, definition, example, synonyms):
        """Adds a card to the Anki deck."""
        
        # Format the back of the card using the requested HTML structure
        back_content = (
            f"{preview_tr}"
            f"<hr>"
            f"{definition}"
            f"<br><br>"
            f"<b>Ex:</b> {example}"
            f"<br><br>"
            f"<b>Synonyms:</b> {synonyms}"
        )

        note = {
            "deckName": self.deck_name,
            "modelName": "Basic",
            "fields": {
                "Front": word,
                "Back": back_content
            },
            "options": {
                "allowDuplicate": False
            },
            "tags": ["anki_ai_automator"]
        }

        try:
            self._invoke("addNote", note=note)
            return True, "Success"
        except Exception as e:
            return False, str(e)
