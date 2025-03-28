from transformers import pipeline

classifier = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")

with open("/data/input.txt", "r", encoding="utf-8") as f:
    text = f.read()

result = classifier(text)[0]
sentiment = result["label"]
confidence = round(result["score"] * 100, 2)

print(f"Sentiment: {sentiment.upper()} (Confidence: {confidence}%)")
