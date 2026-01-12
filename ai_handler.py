import os
import google.generativeai as genai

class AIHandler:
    def __init__(self, api_key=None):
        # User's Google AI Studio Key (ending in JN00 based on previous context/screenshot)
        self.api_key = api_key or "AIzaSyCAPhDWXrReU3v1Q00Zuh0IIBpwPsvD2oo"
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            # Using 'gemini-flash-latest' which is verified to be available
            self.model = genai.GenerativeModel('gemini-flash-latest') 
        else:
            self.model = None

    def enhance_text(self, text):
        if not self.model:
            return "Error: No Gemini API Key provided."

        if not text or len(text.strip()) < 2:
            return ""

        try:
            prompt = f"Rewrite the following text to be polished, professional, and clear. Improve the flow and articulation. Keep the length reasonable (medium) - do not make it overly short, but do not write a whole paragraph for a simple sentence. Avoid unnecessary fluff. Just provide the enhanced text. Input text: '{text}'"
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            # Fallback if primary is not available (404) or quota exceeded (429)
            error_str = str(e).lower()
            if "404" in error_str or "not found" in error_str or "429" in error_str or "quota" in error_str:
                try:
                    # Fallback to gemini-pro-latest which is verified to be available
                    fallback_model = genai.GenerativeModel('gemini-pro-latest')
                    response = fallback_model.generate_content(prompt)
                    return response.text.strip()
                except Exception as e2:
                    return f"AI Error (Fallback): {str(e2)}"
            return f"AI Error: {str(e)}"
