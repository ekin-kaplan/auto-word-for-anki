import os
import json
from google import genai
from dotenv import load_dotenv

class GeminiHandler:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in .env file.")
        
        self.client = genai.Client(api_key=api_key)
        self.model_name = 'models/gemini-flash-latest'

    def generate_card_content(self, word):
        """Generates flashcard content for the given word."""
        
        prompt = f"""
        You are an expert English teacher for Turkish students.
        I will give you an English word: "{word}".
        
        You must return a strictly valid JSON object. Do not include any markdown formatting like ```json ... ```. Just the raw JSON string.
        The JSON object must have exactly these keys:
        
        1. "preview_tr": A string containing the Turkish translation followed by a creative/memorable analogy in Turkish. 
           Format: "Turkish Translation (Analogy)"
           Example: "Serendipity - Şans eseri bulunan mutlu tesadüf (Aradığın kitabı bulamayıp, rastgele eline aldığın kitabın hayatını değiştirmesi gibi)"
           
        2. "english_definition": A formal definition in English, similar to Cambridge Dictionary.
        
        3. "example_sentence": A clear example sentence in English using the word.
        
        4. "synonyms": A string containing 3-5 synonyms, separated by commas.
        
        Strictly adhere to this format.
        """
        
        try:
            print(f"DEBUG: Generating content with active model: {self.model_name}")
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config={'response_mime_type': 'application/json'}
            )
            
            # Clean up potential markdown formatting if the model disregards instructions
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            
            data = json.loads(text)
            
            # validate keys
            required_keys = ["preview_tr", "english_definition", "example_sentence", "synonyms"]
            for key in required_keys:
                if key not in data:
                    raise KeyError(f"Missing key in response: {key}")
                    
            return data
            
        except Exception as e:
            print(f"DEBUG: Error generating content: {e}")
            error_str = str(e)
            if "429" in error_str or "ResourceExhausted" in error_str:
                 return {"error": "Ücretsiz kullanım limitine ulaştınız. Lütfen birkaç dakika bekleyip tekrar deneyiniz."}
            else:
                 return {"error": "Bağlantı hatası oluştu. İnternetinizi kontrol edin."}
