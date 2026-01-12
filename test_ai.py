from ai_handler import AIHandler
import os

print("Initializing AIHandler...")
handler = AIHandler()
# Using a simple prompt that should yield a short answer if concise, but a long answer if detailed.
text = "plan a date" 
print(f"Enhancing text: '{text}'")
result = handler.enhance_text(text)
print("-" * 20)
print("Result:")
print(result)
print("-" * 20)
