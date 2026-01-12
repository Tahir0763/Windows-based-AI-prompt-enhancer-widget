import google.generativeai as genai
import os

api_key = "AIzaSyCAPhDWXrReU3v1Q00Zuh0IIBpwPsvD2oo"
genai.configure(api_key=api_key)

print("Listing available models...")
try:
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(f"Name: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
