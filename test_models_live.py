import google.generativeai as genai
import time

api_key = "AIzaSyCAPhDWXrReU3v1Q00Zuh0IIBpwPsvD2oo"
genai.configure(api_key=api_key)

candidates = [
    "gemini-1.5-flash",
    "gemini-1.5-flash-001",
    "gemini-1.5-flash-002",
    "gemini-1.5-flash-8b",
    "gemini-1.5-pro",
    "gemini-pro",
    "gemini-1.0-pro"
]

print("Testing models for generation success...")

for model_name in candidates:
    print(f"Testing {model_name}...", end=" ", flush=True)
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hi")
        print(f"SUCCESS! Response: {response.text.strip()}")
        print(f"!!! FOUND WORKING MODEL: {model_name} !!!")
        break
    except Exception as e:
        print(f"FAILED: {e}")
        time.sleep(1) # avoidance rate limit spacing
