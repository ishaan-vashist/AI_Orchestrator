import re

with open("/data/input.txt", "r", encoding="utf-8") as f:
    text = f.read()

# Basic text cleaning
text = text.strip()
text = re.sub(r"\s+", " ", text)  # Normalize all whitespace
text = text.replace("—", "-")     # Replace em-dash with dash
text = text.replace("\n", " ")    # Remove newlines

print(text)
