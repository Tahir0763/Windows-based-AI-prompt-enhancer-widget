import google.generativeai as genai
import os

# Use the key from the code if env var not set, for safety
key = "AIzaSyCAPhDWXrReU3v1Q00Zuh0IIBpwPsvD2oo"
genai.configure(api_key=key)

print("Listing available models:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
